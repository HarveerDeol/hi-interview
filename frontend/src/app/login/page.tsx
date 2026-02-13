"use client";

import { Button, PasswordInput, TextInput, Title } from "@mantine/core";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { AxiosError } from "axios";

import { useApi } from "@/api/context";
import { ApiError } from "@/types";
import { AUTHED_HOMEPAGE } from "@/constants";

import styles from "./page.module.scss";

export default function LoginPage() {
    const router = useRouter();
    const api = useApi();

    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [authenticating, setAuthenticating] = useState<boolean>(false);
    const [error, setError] = useState<string>("");

    const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!email || !password) return;
        if (authenticating) return;

        setAuthenticating(true);
        setError("");
        api.login(email, password)
            .then(() => router.push(AUTHED_HOMEPAGE))
            .catch((requestError: AxiosError) => {
                const errorData = requestError.response?.data as ApiError;
                setError(errorData?.detail || "Something went wrong");
            })
            .finally(() => setAuthenticating(false));
    };

    return (
        <div className={styles.background}>
            <form
                onSubmit={handleLogin}
                className={styles.form}
            >
                <Title
                    order={3}
                    className={styles.title}
                >
                    Hi Interview
                </Title>
                <TextInput
                    label="Email"
                    placeholder="Your email"
                    required
                    value={email}
                    onChange={event => setEmail(event.target.value)}
                    classNames={{
                        input: styles.input,
                        label: styles.label,
                    }}
                    autoComplete="off"
                    autoCapitalize="none"
                    autoCorrect="off"
                />
                <PasswordInput
                    label="Password"
                    placeholder="Your password"
                    required
                    value={password}
                    onChange={event => setPassword(event.target.value)}
                    classNames={{
                        input: styles.input,
                        label: styles.label,
                    }}
                    autoComplete="off"
                    autoCapitalize="none"
                    autoCorrect="off"
                    className={styles["password-input"]}
                />
                {error && <p className={styles.error}>{error}</p>}
                <Button
                    disabled={!email || !password || authenticating}
                    type="submit"
                    className={styles["submit-button"]}
                >
                    Sign in
                </Button>
            </form>
        </div>
    );
}
