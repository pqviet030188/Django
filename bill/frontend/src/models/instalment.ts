export type InstalmentStatus = 'paid' | 'unpaid';

export interface Instalment {
    id: number,
    bill_id: number,
    amount: number,
    due: string,
    status: InstalmentStatus
}

export interface InstalmentListResponse {
    results: Array<Instalment>
}