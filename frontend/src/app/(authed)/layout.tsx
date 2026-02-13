"use client";

import NavigationMenu from "./components/NavigationMenu";

interface ComponentProps {
    children: React.ReactNode;
}

export default function AuthedLayout({ children }: ComponentProps) {
    return <NavigationMenu>{children}</NavigationMenu>;
}
