import { useCallback, useEffect, useState } from "react";
import {
  Bill,
  BillImage,
  BillListResponse,
  Instalment,
  InstalmentListResponse,
} from "../models";
import { Config } from "../config";
import axios from "axios";
import { getEmptyArray } from "../constants";
import { useApi } from "./useApi";

const mergedUnique = (bills: Bill[]) => {
  return bills;
  const seen = new Set<number>();
  const result: Bill[] = [];

  for (const item of bills) {
    if (!seen.has(item.id)) {
      seen.add(item.id);
      result.push(item);
    }
  }

  return result;
};

const fetchBills = async (cursor: number | null | undefined) => {
  const limit = 10;
  try {
    const data = await axios
      .get<BillListResponse>(
        `${Config.API_ENDPOINT}/bills?limit=${limit}&${
          cursor != null ? `cursor=${cursor}` : ``
        }`,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        return {
          results:
            response?.data?.results?.map((d) => {
              return {
                ...d,
                images: [
                  ...(d?.images?.map((d) => {
                    return {
                      ...d,
                      image: `${Config.API_ENDPOINT}${d.image}`,
                    } as BillImage;
                  }) ?? getEmptyArray<BillImage>()),
                ],
              };
            }) ?? getEmptyArray<Bill>(),
          next_cursor: response?.data?.next_cursor ?? null,
        };
      })
      .catch((err) => {
        console.log(err);
        return null;
      });

    if (data) {
      const instalments = await Promise.all(
        data?.results?.map((d) => {
          return axios
            .get<InstalmentListResponse>(
              `${Config.API_ENDPOINT}/bills/${d.id}/all-instalments`,
              {
                headers: {
                  "Content-Type": "application/json",
                },
              }
            )
            .then((response) => {
              return response?.data?.results ?? getEmptyArray<Instalment>();
            })
            .catch((err) => {
              console.log(err);
              return getEmptyArray<Instalment>();
            });
        })
      );

      data.results = data?.results?.map((d, index) => {
        return {
          ...d,
          instalments: instalments[index] ?? getEmptyArray<Instalment>(),
        };
      });
      return data;
    }
  } catch (err) {
    console.log(err);
  }

  return null;
};

export const useBillData = () => {
  const [billData, setBillData] = useState<
    BillListResponse & {
      loading: boolean;
    }
  >({
    loading: false,
    next_cursor: null,
    results: [],
  });

  const _fetchBills = useApi(fetchBills);
  const fetchBillsWithCursor = useCallback(async () => {
    try {
      setBillData((prev) => {
        return {
          ...prev,
          loading: true,
        };
      });
      const newBillData = await _fetchBills(billData?.next_cursor);
      if (newBillData) {
        setBillData((prev) => {
          return {
            ...prev,
            results: mergedUnique([
              ...(prev.results ?? getEmptyArray<Bill>()),
              ...(newBillData.results ?? getEmptyArray<Bill>()),
            ]),
            next_cursor: newBillData.next_cursor ?? prev?.next_cursor,
          };
        });
      }
    } catch (err) {
      console.log(err);
    } finally {
       setBillData((prev) => {
        return {
          ...prev,
          loading: false,
        };
      });
    }
  }, [billData?.next_cursor, setBillData, _fetchBills]);

  // scroll listener
  useEffect(() => {
    const handleScroll = () => {
      const bottomReached =
        window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;

      if (bottomReached && !billData?.loading) {
        fetchBillsWithCursor();
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [fetchBillsWithCursor, billData?.loading]);

  useEffect(() => {
    fetchBillsWithCursor();
  
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return billData;
};
