import { PropsWithChildren } from 'react';
import { PageWrapperStyled } from './PageWrapper.styles';

function PageWrapper({ children }: PropsWithChildren) {
  return <PageWrapperStyled>{children}</PageWrapperStyled>;
}

export default PageWrapper;
