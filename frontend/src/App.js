import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React from 'react';
import orderBy from 'lodash/orderBy';

const baseURL = 'http://localhost:8000/';

function App() {
  const [orders, setOrders] = React.useState([]);
  React.useEffect(() => {
    axios.get(baseURL + 'app/orders/').then(
      response => setOrders(response.data)
    );
  }
    , []);

  if (orders.length === 0) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <table className="result-table">
          <thead>
            <tr>
              <td className="table-cell">№</td>
              <td className="table-cell">Заказ №</td>
              <td className="table-cell">Стоимость $</td>
              <td className="table-cell">Срок поставки</td>
              <td className="table-cell">Стоимость в Руб.</td>
            </tr>
          </thead>
          <tbody>
            {orderBy(orders, ['index_in_table']).map(order => (<tr key={order.order_id.toString()}>
              <td className="table-cell">{order.index_in_table}</td>
              <td className="table-cell">{order.order_id}</td>
              <td className="table-cell">{order.total_cost_in_dollars}</td>
              <td className="table-cell">{order.incoming_date}</td>
              <td className="table-cell">{order.total_cost_in_rubles}</td>
            </tr>))}
          </tbody>
        </table>
      </header>
    </div>
  );
}

export default App;
