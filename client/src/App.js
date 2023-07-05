import React, { Component } from 'react';
import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from 'react-router-dom';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import PageNotFound from './components/page_not_found'
import SignIn from './components/signin'
import Signup from './components/signup'
import Dashboard from './components/dashboard'
import Web3 from 'web3'
import {Blockchain_Address} from './blockchain_address'

class App extends Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: ''
    };
  }

  componentDidMount() {

  }

  componentWillMount() {
    this.loadBlockchainData()
  }

  async loadBlockchainData() {
    const web3 = new Web3(Blockchain_Address)
    const accounts = await web3.eth.getAccounts()
    this.setState({ account: accounts[0] })
    console.log('List of accounts:', accounts)
  }

  render() {
    return (
      <div className="App" style={{}}>
        <BrowserRouter>
            <Routes>
              <Route path='/' element={<SignIn />}/>
              <Route path='/signup' element={<Signup />}/>
              <Route path='/dashboard' element={<Dashboard />}/>
              <Route path="*" element={<PageNotFound />} />
            </Routes>
        </BrowserRouter>    
      </div>
    );
  }
}

export default withCookies(App);
