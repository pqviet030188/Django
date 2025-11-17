import { PageWrapper } from '@components/PageWrapper';
import { useBillData } from '../../hooks';
import { BillList } from './BillList';

function BillListWithLoader() {
  const {results} = useBillData();
  return (
    <PageWrapper>
     <BillList bills={results}/>
    </PageWrapper>
  );
}

export default BillListWithLoader;
