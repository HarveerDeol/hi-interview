import { AxiosInstance } from "axios";
import { Client, Note } from "@/types/clients";

export default class ClientsApi {
    private axiosInstance: AxiosInstance;

    constructor(axiosInstance: AxiosInstance) {
        this.axiosInstance = axiosInstance;
    }

    public listClients = async (): Promise<Client[]> => {
        const response = await this.axiosInstance.get<{ data: Client[] }>("client");
        return response.data.data;
    };

    public getClient = async (clientId: string): Promise<Client> => {
        const response = await this.axiosInstance.get<Client>(`client/${clientId}`);
        return response.data;
    };

    public listNotes = async (clientId: string): Promise<Note[]> => {
        const response = await this.axiosInstance.get<{ data: Note[] }>(`client/${clientId}/note`);
        return response.data.data;
    };

    public createNote = async (clientId: string, content: string): Promise<Note> => {
        const response = await this.axiosInstance.post<Note>(`client/${clientId}/note`, { content });
        return response.data;
    };
}