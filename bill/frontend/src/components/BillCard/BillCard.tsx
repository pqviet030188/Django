import { InstalmentCard } from '@components/Instalment';
import { BillCardProps } from './BillCard.interface';
import { BillCardContentContainerStyled, BillCardImageStyled, BillCardInstalmentsContainerStyled, BillCardStyled } from './BillCard.styles';
import { BillCardContent } from './BillCardContent';

function BillCard({ bill }: BillCardProps) {
  return <BillCardStyled>
    <BillCardImageStyled 
      src={bill?.images?.[0]?.image}
    ></BillCardImageStyled>
    
    <BillCardContentContainerStyled>
      <BillCardContent bill={bill}></BillCardContent>
    </BillCardContentContainerStyled>

    <BillCardInstalmentsContainerStyled>
      {
        bill?.instalments?.map(instalment=>{
          return <InstalmentCard instalment={instalment} key={instalment.id}></InstalmentCard>
        })
      }
    </BillCardInstalmentsContainerStyled>
  </BillCardStyled>;
}

export default BillCard;
