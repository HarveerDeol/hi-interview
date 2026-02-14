"use client";

import { Button, Group, Stack, Text, Textarea, Title } from "@mantine/core";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { useApi } from "@/api/context";
import { Client, Note } from "@/types/clients";

import styles from "./page.module.scss";

export default function ClientDetailPage() {
    const api = useApi();
    const params = useParams();
    const id = typeof params?.id === "string" ? params.id : undefined;
    const router = useRouter();

    const [client, setClient] = useState<Client | null>(null);
    const [loading, setLoading] = useState(true);

    const [notes, setNotes] = useState<Note[]>([]);
    const [notesLoading, setNotesLoading] = useState(true);
    const [noteContent, setNoteContent] = useState("");
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        if (!id) {
            setLoading(false);
            return;
        }
        api.clients
            .getClient(id)
            .then(setClient)
            .catch(() => setClient(null))
            .finally(() => setLoading(false));

        api.clients
            .listNotes(id)
            .then(setNotes)
            .finally(() => setNotesLoading(false));
    }, [api, id]);

    const handleCreateNote = () => {
        if (!id || !noteContent.trim()) return;
        setSubmitting(true);
        api.clients
            .createNote(id, noteContent.trim())
            .then((note) => {
                setNotes([note, ...notes]);
                setNoteContent("");
            })
            .finally(() => setSubmitting(false));
    };

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
                <Button variant="light" onClick={() => router.back()}>
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

            <Title order={3} mt="xl" mb="md">
                Notes
            </Title>

            <Stack gap="sm" mb="xl">
                <Textarea
                    placeholder="Add a note..."
                    value={noteContent}
                    onChange={(e) => setNoteContent(e.currentTarget.value)}
                    minRows={3}
                />
                <Button
                    onClick={handleCreateNote}
                    disabled={!noteContent.trim() || submitting}
                    loading={submitting}
                >
                    Add Note
                </Button>
            </Stack>

            {notesLoading ? (
                <Text>Loading notes...</Text>
            ) : notes.length === 0 ? (
                <Text c="dimmed">No notes yet.</Text>
            ) : (
                <Stack gap="md">
                    {notes.map((note) => (
                        <Stack key={note.id} gap="xs" className={styles.note}>
                            <Text size="sm">{note.content}</Text>
                            <Text size="xs" c="dimmed">
                                {new Date(note.created_at).toLocaleString()}
                            </Text>
                        </Stack>
                    ))}
                </Stack>
            )}
        </div>
    );
}