from pyteal import *


router = Router(
    "FamilyInsurance",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
        opt_in=OnCompleteAction.always(Approve()),
        close_out=OnCompleteAction.always(Approve()),
        update_application=OnCompleteAction.never(),
        delete_application=OnCompleteAction.never(),
    ),
)


# Global keys
KEY_POLICY_ID = Bytes("policyId")
KEY_WALLET = Bytes("wallet")
KEY_COVERAGE = Bytes("coverage")
KEY_STATUS = Bytes("status")
KEY_EXPIRY = Bytes("expiry")
KEY_CLAIM_STATUS = Bytes("claimStatus")


@router.method
def createPolicy(
    policyId: abi.String,
    walletAddress: abi.String,
    coverageAmount: abi.Uint64,
    status: abi.String,
    expiryDate: abi.String,
    claimStatus: abi.String,
) -> Expr:
    return Seq(
        App.globalPut(KEY_POLICY_ID, policyId.get()),
        App.globalPut(KEY_WALLET, walletAddress.get()),
        App.globalPut(KEY_COVERAGE, coverageAmount.get()),
        App.globalPut(KEY_STATUS, status.get()),
        App.globalPut(KEY_EXPIRY, expiryDate.get()),
        App.globalPut(KEY_CLAIM_STATUS, claimStatus.get()),
        Approve(),
    )


@router.method
def verifyPolicy(output: abi.Bool) -> Expr:
    return Seq(
        output.set(App.globalGet(KEY_STATUS) == Bytes("active")),
        Approve(),
    )


@router.method
def submitClaim(claimStatus: abi.String) -> Expr:
    return Seq(
        App.globalPut(KEY_CLAIM_STATUS, claimStatus.get()),
        Approve(),
    )


@router.method
def approveClaim(claimStatus: abi.String, policyStatus: abi.String) -> Expr:
    return Seq(
        App.globalPut(KEY_CLAIM_STATUS, claimStatus.get()),
        App.globalPut(KEY_STATUS, policyStatus.get()),
        Approve(),
    )


def get_contract_artifacts():
    approval_program, clear_program, contract = router.compile_program(version=8)
    return {
        "approval": approval_program,
        "clear": clear_program,
        "abi": contract.dictify(),
    }
