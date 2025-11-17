import { Instalment } from "./instalment";

export type BillStatus = 'processing' | 'scheduled' | 'unable_to_pay' | 'paid';

export interface BillImage {
    id: number,
    image: string
}

export interface Bill {
    id: number,
    biller: string,
    amount: number,
    date: string,
    status: BillStatus,
    status_context: string,
    images: Array<BillImage>,
    instalments: Array<Instalment>
}

export interface BillListResponse {
    results: Array<Bill>,
    next_cursor: number | null | undefined
}