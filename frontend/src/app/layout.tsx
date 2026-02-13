import type { Metadata } from "next";
import { ColorSchemeScript, MantineProvider } from "@mantine/core";

import { ApiProvider } from "@/api/context";
import { theme } from "@/theme";

import "./globals.css";

export const metadata: Metadata = {
    title: "Hi Interview",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html
            lang="en"
            suppressHydrationWarning
        >
            <head>
                <ColorSchemeScript />
            </head>
            <body>
                <MantineProvider theme={theme}>
                    <ApiProvider>{children}</ApiProvider>
                </MantineProvider>
            </body>
        </html>
    );
}
