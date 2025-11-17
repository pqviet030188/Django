import { FC } from "react";
import { Instalment } from "../../models";
import {
  InstalmentCardStyled,
  InstalmentLineItemStyled,
} from "./Instalment.styles";

interface InstalmentProps {
  instalment: Instalment;
}

export const InstalmentCard: FC<InstalmentProps> = ({ instalment }) => {
  return (
    <InstalmentCardStyled>
      <InstalmentLineItemStyled>Instalment: {instalment.id}</InstalmentLineItemStyled>
      <InstalmentLineItemStyled>Due: {instalment.due}</InstalmentLineItemStyled>
      <InstalmentLineItemStyled>Status: {instalment.status}</InstalmentLineItemStyled>
    </InstalmentCardStyled>
  );
};