import "@styles/globals.css";

import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  // description: "...",
  title: "CX Hackathon 2024",
};

const RootLayout = ({ children }: { children: ReactNode }) => {
  return (
    <html lang="en">
      <body>
        {/* <header> */}
        {/*   <nav>navigation here...</nav> */}
        {/* </header> */}

        {/* Layout UI */}
        <main className="flex flex-col m-4 items-center">{children}</main>

        {/* <footer>footer here...</footer> */}
      </body>
    </html>
  );
};

export default RootLayout;
