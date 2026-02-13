"use client";

import { useEffect, useState } from "react";
import { AppShell, Loader, Text } from "@mantine/core";
import { IconLogout, IconUsers } from "@tabler/icons-react";
import { usePathname, useRouter } from "next/navigation";

import { useApi } from "@/api/context";

import styles from "./NavigationMenu.module.scss";

export default function NavigationMenu({
    children,
}: {
    children: React.ReactNode;
}) {
    const api = useApi();
    const router = useRouter();
    const pathname = usePathname();
    const [authenticating, setAuthenticating] = useState(true);

    useEffect(() => {
        api.checkAuth()
            .then(authenticated => {
                if (!authenticated) router.replace(`/login?next=${pathname}`);
            })
            .finally(() => setAuthenticating(false));
    }, [api, router, pathname]);

    const handleLogout = () => {
        api.resetAuth().then(() => {
            router.push("/login");
        });
    };

    return (
        <AppShell
            padding="0"
            withBorder={false}
            classNames={{ root: styles.root }}
            navbar={{
                width: 160,
                breakpoint: "sm",
            }}
        >
            <AppShell.Navbar className={styles["nav-bar"]}>
                <AppShell.Section grow>
                    <div
                        className={
                            styles["nav-button"] +
                            (pathname?.startsWith("/clients")
                                ? " " + styles["nav-button-selected"]
                                : "")
                        }
                        onClick={() => router.push("/clients")}
                    >
                        <IconUsers size={18} />
                        <Text size="md">Clients</Text>
                    </div>
                </AppShell.Section>
                <AppShell.Section>
                    <div
                        className={styles["nav-button"]}
                        onClick={handleLogout}
                    >
                        <IconLogout size={18} />
                        <Text size="md">Logout</Text>
                    </div>
                </AppShell.Section>
            </AppShell.Navbar>
            <AppShell.Main className={styles.main}>
                {authenticating ? (
                    <div className={styles.loading}>
                        <Loader
                            variant="bars"
                            size="lg"
                        />
                    </div>
                ) : (
                    children
                )}
            </AppShell.Main>
        </AppShell>
    );
}
