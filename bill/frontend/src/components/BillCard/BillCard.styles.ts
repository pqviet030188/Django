import styled from 'styled-components';

export const BillCardStyled = styled.div`
  display: flex;
  align-items: center;
  flex-direction: row;
  gap: 20px;
  border: 1px solid #000;
  border-radius: 8px;
  color: #000;
  background-color: #fff;
  margin: 10px 0px;
`;

export const BillCardImageStyled = styled.img`
  flex-basis: 30%;
  max-width: 500px;
  max-height: 500px;
  flex: 0 0;
`;

export const BillCardContentContainerStyled = styled.div`
  flex: 0 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  flex-basis: 250px;
`;

export const BillCardInstalmentsContainerStyled = styled.div`
  display: flex;
  flex: 1;
  flex-direction: row;
  gap: 20px;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
  margin: 10px 0;
`;