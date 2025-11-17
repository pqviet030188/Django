import { act, render, RenderResult, screen } from "@testing-library/react";
import BillListWithLoader from "../BillListWithLoader";
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { BillListResponse, InstalmentListResponse } from "../../../models";

import { fireEvent } from "@testing-library/react";

export function scrollToBottom() {
  // mock window scroll properties
  window.innerHeight = 1000;
  Object.defineProperty(document.documentElement, "scrollHeight", {
    configurable: true,
    get: () => 2000,
  });
  window.pageYOffset = 1000;

  fireEvent.scroll(window);
}

const bills = new Array(22).fill(0).map((_, index) => {
  return {
    id: index,
    biller: `Bill ${index}`,
    amount: 100,
    date: "15/06/2025",
    status: "paid",
    status_context: "status_context_value",
    images: [
      {
        id: 1,
        image: "/media/test.png",
      },
    ],
  };
});

const handlers = [
  http.get("http://localhost:8000/bills", ({ request }) => {
    const url = new URL(request.url);
    const params = url.searchParams;
    const limit = params.get("limit");
    const cursor = params.get("cursor");
    const results = bills
      .filter((b, index) => {
        return cursor == null ? index > -1 : b.id > parseInt(cursor);
      })
      .slice(0, limit == null ? 10 : parseInt(limit));

    return HttpResponse.json({
      results,
      next_cursor: results?.[(results?.length ?? 0) - 1]?.id,
    } as BillListResponse);
  }),
  http.get(
    "http://localhost:8000/bills/:billId/all-instalments",
    ({ params }) => {
      const { billId } = params;
      const results = [
        {
          bill_id: parseInt(billId as string),
          amount: 20,
          due: "15/06/2025",
          id: parseInt(billId as string) + 10,
          status: "paid",
        },
      ];

      return HttpResponse.json({
        results,
      } as InstalmentListResponse);
    }
  ),
];

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("BillList", () => {
  it("should render correctly", async() => {
    let container: RenderResult | null = null;
    await act(async () => {
      // fire some event that triggers async state update
      container = render(<BillListWithLoader />);
    });
    expect(container).not.toBeFalsy();
    expect(container).toMatchSnapshot();
  });

  it("should contain header", () => {
    render(<BillListWithLoader />);
    const header = screen.getByText("Bill List");
    expect(header).toBeVisible();
  });

  it("should contain 10 bills at start", async () => {
    await act(async () => {
      // fire some event that triggers async state update
      render(<BillListWithLoader />);
    });
    const billerNames = screen.getAllByText(/^Biller: Bill \d+$/);
    expect(billerNames?.length).toBe(10);
    billerNames.forEach((bill) => {
      expect(bill).toBeVisible();
    });
  });

  it("should contain 20 bills after 1st scroll", async () => {
    await act(async () => {
      // fire some event that triggers async state update
      render(<BillListWithLoader />);
    });

    await act(async () => {
      scrollToBottom();
    });

    const billerNames = screen.getAllByText(/^Biller: Bill \d+$/);
    expect(billerNames?.length).toBe(20);
    billerNames.forEach((bill) => {
      expect(bill).toBeVisible();
    });
  });

  it("should contain 22 bills after 2nd scroll", async () => {
    await act(async () => {
      // fire some event that triggers async state update
      render(<BillListWithLoader />);
    });

    await act(async () => {
      scrollToBottom();
    });

    await act(async () => {
      scrollToBottom();
    });

    const billerNames = screen.getAllByText(/^Biller: Bill \d+$/);
    expect(billerNames?.length).toBe(22);
    billerNames.forEach((bill) => {
      expect(bill).toBeVisible();
    });
  });

  it("should contain 22 bills after 3rd scroll", async () => {
    await act(async () => {
      // fire some event that triggers async state update
      render(<BillListWithLoader />);
    });

    await act(async () => {
      scrollToBottom();
    });

    await act(async () => {
      scrollToBottom();
    });

     await act(async () => {
      scrollToBottom();
    });

    const billerNames = screen.getAllByText(/^Biller: Bill \d+$/);
    expect(billerNames?.length).toBe(22);
    billerNames.forEach((bill) => {
      expect(bill).toBeVisible();
    });
  });

  it("should contain 20 bills after repeatedly scrolling to the bottom", async () => {
    await act(async () => {
      // fire some event that triggers async state update
      render(<BillListWithLoader />);
    });

    await act(async () => {
      scrollToBottom();
      scrollToBottom();
      scrollToBottom();
      scrollToBottom();
    });

    const billerNames = screen.getAllByText(/^Biller: Bill \d+$/);
    expect(billerNames?.length).toBe(20);
    billerNames.forEach((bill) => {
      expect(bill).toBeVisible();
    });
  });
});
