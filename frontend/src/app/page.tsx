"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader } from "@mantine/core";

import { useApi } from "@/api/context";
import { AUTHED_HOMEPAGE } from "@/constants";

import styles from "./page.module.scss";

export default function Page() {
    const router = useRouter();
    const api = useApi();

    useEffect(() => {
        api.checkAuth().then(authenticated => {
            if (authenticated) {
                router.push(AUTHED_HOMEPAGE);
            } else {
                router.push("/login");
            }
        });
    }, [api, router]);

    return (
        <div className={styles.loading}>
            <Loader
                variant="bars"
                size="lg"
            />
        </div>
    );
}
