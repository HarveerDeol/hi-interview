"use client";

import { Button, Group, Stack, Text, Title } from "@mantine/core";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";


import { useApi } from "@/api/context";
import { Client } from "@/types/clients";

import styles from "./page.module.scss";

export default function ClientDetailPage() {
    const api = useApi();
    const params = useParams();
    const id = typeof params?.id === "string" ? params.id : undefined;
    const router = useRouter();
    const [client, setClient] = useState<Client | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.clients
            .getClient(params.id)
            .then(setClient)
            .catch(() => setClient(null))
            .finally(() => setLoading(false));
    }, [api, params.id]);

    if (loading) {
        return <div className={styles.container}>Loading...</div>;
    }

    if (!client) {
        return <div className={styles.container}>Client not found</div>;
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <Title order={2} className={styles.title}>
                    {client.first_name} {client.last_name}
                </Title>
                <Button
                    variant="light"
                    onClick={() => router.back()}
                >
                    Back
                </Button>
            </div>

            <Stack gap="md" className={styles.details}>
                <Group justify="space-between">
                    <Text fw={500}>Email:</Text>
                    <Text>{client.email}</Text>
                </Group>

                <Group justify="space-between">
                    <Text fw={500}>First Name:</Text>
                    <Text>{client.first_name}</Text>
                </Group>

                <Group justify="space-between">
                    <Text fw={500}>Last Name:</Text>
                    <Text>{client.last_name}</Text>
                </Group>

                <Group justify="space-between">
                    <Text fw={500}>Assigned User:</Text>
                    <Text>{client.assigned_user_id || "Unassigned"}</Text>
                </Group>

                <Group justify="space-between">
                    <Text fw={500}>Created:</Text>
                    <Text>{new Date(client.created_at).toLocaleString()}</Text>
                </Group>

                <Group justify="space-between">
                    <Text fw={500}>Updated:</Text>
                    <Text>{new Date(client.updated_at).toLocaleString()}</Text>
                </Group>
            </Stack>
        </div>
    );
}
