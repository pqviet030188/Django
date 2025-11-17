import { BillListContainerStyled, BillListTitle } from './BillList.styles';
import { BillCard } from '@components/BillCard';
import { Bill } from 'src/models';
import { FC } from 'react';

export const BillList: FC<{bills: Bill[]}> = ({
    bills
})=>{
    return (
    <>
      <BillListTitle>Bill List</BillListTitle> 
      <BillListContainerStyled>{bills?.map((bill) => (
        <BillCard bill={bill} key={bill.id} />
      ))}</BillListContainerStyled>
    </>
  );
}