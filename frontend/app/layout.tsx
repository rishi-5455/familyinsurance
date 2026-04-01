import "./globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "Blockchain Enabled Family Insurance",
  description: "Policy enquiry and verification system",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
