"use client";

import { Button, Group, Modal, Table, TextInput, Title } from "@mantine/core";
import { useEffect, useState } from "react";

import { useApi } from "@/api/context";
import { Client } from "@/types/clients";

import { useRouter } from "next/navigation";

import styles from "./page.module.scss";

export default function ClientsPage() {
    const api = useApi();
    const router = useRouter();

    const [clients, setClients] = useState<Client[]>([]);
    const [loading, setLoading] = useState(true);
    const [open, setOpen] = useState(false);
    const [creating, setCreating] = useState(false);
    const [formData, setFormData] = useState({
        email: "",
        firstName: "",
        lastName: "",
    });
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        api.clients.listClients()
            .then(setClients)
            .finally(() => setLoading(false));
    }, [api]);

    const handleCreateClient = async () => {
        if (!formData.email || !formData.firstName || !formData.lastName) {
            setError("All fields are required");
            return;
        }

        setCreating(true);
        setError(null);

        try {
            const newClient = await api.clients.createClient(
                formData.email,
                formData.firstName,
                formData.lastName
            );
            setClients([newClient, ...clients]);
            setOpen(false);
            setFormData({ email: "", firstName: "", lastName: "" });
        } catch (e) {
            setError("Failed to create client");
        } finally {
            setCreating(false);
        }
    };

    if (loading) {
        return <div className={styles.container}>Loading...</div>;
    }

    return (
        <div className={styles.container}>
            <Title
                order={2}
                className={styles.title}
            >
                Clients
            </Title>

            <Button
                onClick={() => setOpen(true)}
                mb="lg"
            >
                Create Client
            </Button>

            <Modal
                opened={open}
                onClose={() => {
                    setOpen(false);
                    setError(null);
                    setFormData({ email: "", firstName: "", lastName: "" });
                }}
                title="Create New Client"
            >
                <TextInput
                    label="Email"
                    placeholder="email@example.com"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.currentTarget.value })}
                    mb="sm"
                />
                <TextInput
                    label="First Name"
                    placeholder="John"
                    value={formData.firstName}
                    onChange={(e) => setFormData({ ...formData, firstName: e.currentTarget.value })}
                    mb="sm"
                />
                <TextInput
                    label="Last Name"
                    placeholder="Doe"
                    value={formData.lastName}
                    onChange={(e) => setFormData({ ...formData, lastName: e.currentTarget.value })}
                    mb="md"
                />
                {error && (
                    <Group mb="md" c="red">
                        {error}
                    </Group>
                )}
                <Group justify="flex-end">
                    <Button
                        variant="light"
                        onClick={() => {
                            setOpen(false);
                            setError(null);
                            setFormData({ email: "", firstName: "", lastName: "" });
                        }}
                    >
                        Cancel
                    </Button>
                    <Button
                        onClick={handleCreateClient}
                        loading={creating}
                        disabled={!formData.email || !formData.firstName || !formData.lastName}
                    >
                        Create
                    </Button>
                </Group>
            </Modal>
            <Table
                striped
                highlightOnHover
                withTableBorder
                withColumnBorders
            >
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Name</Table.Th>
                        <Table.Th>Email</Table.Th>
                        <Table.Th>Assigned</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                    {clients.map((client) => (
                        <Table.Tr
                            key={client.id}
                            onClick={() => router.push(`/clients/${client.id}`)}
                            style={{ cursor: "pointer" }}
                            tabIndex={0}
                            onKeyDown={(e) => {
                                if (e.key === "Enter" || e.key === " ") {
                                    router.push(`/clients/${client.id}`);
                                }
                            }}
                        >
                            <Table.Td>
                                {client.first_name} {client.last_name}
                            </Table.Td>
                            <Table.Td>{client.email}</Table.Td>
                            <Table.Td>
                                {client.assigned_user_id ? "Yes" : "No"}
                            </Table.Td>
                        </Table.Tr>
                    ))}
                </Table.Tbody>

            </Table>
        </div>
    );
}
