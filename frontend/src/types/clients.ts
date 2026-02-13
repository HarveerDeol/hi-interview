export interface Client {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    assigned_user_id: string | null;
    created_at: string;
    updated_at: string;
}
