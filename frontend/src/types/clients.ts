export interface Client {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    assigned_user_id: string | null;
    created_at: string;
    updated_at: string;
}

export interface Note {
    id: string;
    client_id: string;
    created_by_user_id: string;
    content: string;
    created_at: string;
}