import { useCallback } from 'react';
import { Button, HomeTitle } from './Home.styles';
import { useNavigate } from 'react-router';
import { PageWrapper } from '@components/PageWrapper';

function Home() {
  const navigate = useNavigate();

  const handleBillListOnClick = useCallback(() => {
    navigate('/bill-list');
  }, [navigate]);

  return (
    <PageWrapper>
      <HomeTitle>Home</HomeTitle>
      <Button onClick={handleBillListOnClick}>Bill List</Button>
    </PageWrapper>
  );
}

export default Home;
