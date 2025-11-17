import './App.css';
import { RouterProvider } from 'react-router/dom';
import { createBrowserRouter } from 'react-router';
import { Home } from '@pages/Home';
import { BillList } from '@pages/BillList';

const router = createBrowserRouter([
  {
    path: '/',
    Component: Home,
  },
  {
    path: '/bill-list',
    Component: BillList,
  },
]);

function App() {
  return <RouterProvider router={router}></RouterProvider>;
}

export default App;
