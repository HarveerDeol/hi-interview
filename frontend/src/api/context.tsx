"use client";

import { ReactNode, createContext, useContext } from "react";

import Api from "./Api";

const ApiContext = createContext<Api | undefined>(undefined);

export const ApiProvider = ({ children }: { children: ReactNode }) => {
    const api = new Api();
    return <ApiContext.Provider value={api}>{children}</ApiContext.Provider>;
};

export const useApi = () => {
    const context = useContext(ApiContext);
    if (context === undefined) {
        throw new Error("useApi must be used within an ApiProvider");
    }
    return context;
};
