import { FC, Fragment } from "react";
import { Bill } from "../../models";
import styled from "styled-components";

export const BillCardContentLineItemStyled = styled.div`
  white-space: nowrap;
  text-align: left;
`;

export const BillCardContentMoreInformationStyled = styled.div`
  text-align: left;
`;

export const BillCardContent: FC<{ bill: Bill }> = ({ bill }) => {
  return (
    <Fragment>
      <BillCardContentLineItemStyled>
        Biller: {bill.biller}
      </BillCardContentLineItemStyled>
      <BillCardContentLineItemStyled>
        Due: {bill.date}
      </BillCardContentLineItemStyled>
      <BillCardContentLineItemStyled>
        Amount: ${bill.amount}
      </BillCardContentLineItemStyled>
      <BillCardContentLineItemStyled>
        Status: {bill.status}
      </BillCardContentLineItemStyled>
      <BillCardContentMoreInformationStyled>
        More information: {bill.status_context}
      </BillCardContentMoreInformationStyled>
    </Fragment>
  );
};
