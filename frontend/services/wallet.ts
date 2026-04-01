"use client";

import { PeraWalletConnect } from "@perawallet/connect";

const peraWallet = new PeraWalletConnect();

export const connectPeraWallet = async (): Promise<string | null> => {
  try {
    const accounts = await peraWallet.connect();
    return accounts?.[0] || null;
  } catch {
    return null;
  }
};

export const disconnectPeraWallet = async () => {
  await peraWallet.disconnect();
};
