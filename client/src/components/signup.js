import React, { Component, useReducer } from 'react';
import {Collapse, SignupToggler,SignupBrand,Nav,NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Form, Container, Label, InputGroup} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import {Helmet} from 'react-helmet'
import SignupImage from '../images/signup.png'
import Web3 from 'web3'
import {Blockchain_Address} from '../blockchain_address'
import { VOTERS_ABI, VOTERS_ADDRESS, ELECTIONS_ABI, ELECTIONS_ADDRESS, VOTES_ABI, VOTES_ADDRESS, STAFF_ABI, STAFF_ADDRESS } from '../config'
import { FaKeybase } from 'react-icons/fa';

class Signup extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: '',
      staff: [],
      firstname: '',
      lastname: '',
      username: '',
      password: ''
    };

    this.HandleChange = (e) =>{
      this.setState({[e.target.name]: e.target.value});
    };

    this.Signup = (e) => {
      e.preventDefault()
      const { cookies } = this.props
      var firstname = this.state.firstname
      var lastname = this.state.lastname
      var username = this.state.username
      var password = this.state.password
      var username_matches = this.state.staff.filter(item => item.username.toLowerCase() == username.toLowerCase())
      
      if (firstname == ''){
        alert('Firstname is required')
      }else if (lastname == ''){
        alert('Lastname is required')
      }else if (username == ''){
        alert('Username is required')
      }else if (username_matches.length > 0){
        alert('Username already registered')
      }else if(password == ''){
        alert('Password is required')
      }else{
        this.setState({ loading: true })
        this.state.contract.methods.create(firstname, lastname, username, password).send({ from: this.state.account })
        .once('receipt', (receipt) => {
          alert('Signup successful')
          this.setState({ loading: false })
          let port = (window.location.port ? ':' + window.location.port : '')
          window.location.href = '//' + window.location.hostname + port + '/signin'
        })
      }
    }
    
  }
  
  componentDidMount() {
    const { cookies } = this.props;
    if(cookies.get('token')!=null){
      let port = (window.location.port ? ':' + window.location.port : '');
      window.location.href = '//' + window.location.hostname + port + '/overview';
    }
  }
  
  componentWillMount() {
    this.loadBlockchainData()
  }

  async loadBlockchainData() {
    // connect to the blockchain
    const web3 = new Web3(Blockchain_Address)
    // get account information
    const accounts = await web3.eth.getAccounts()
    this.setState({ account: accounts[0] })
    console.log('List of accounts:', accounts)
    // get staff (users) contract and set to state
    const contract = new web3.eth.Contract(STAFF_ABI, STAFF_ADDRESS)
    this.setState({ contract })
    // get items count and set to state
    const itemsCount = await contract.methods.itemsCount().call()
    this.setState({ itemsCount })
    // populate state with items
    for (var i = 1; i <= itemsCount; i++) {
      const item = await contract.methods.items(i).call()
      // set data to staff state
      this.setState({
        staff: [...this.state.staff, item]
      })
    }
  }

  render() {
    return (
      <div>
        <Helmet>
          <title>Sign Up | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <Row style={{margin: '0px', minHeight: '630px'}}>
          <Col style={{backgroundColor: '#ffffff', minHeight: '630px'}}>
            <br/><br/><br/>
            <img src={SignupImage} style={{width: '70%'}} />
          </Col>
          <Col sm='6' style={{backgroundColor: '#ffffff'}}>
            <br/><br/>
            <h4 style={{color: '#1faced', fontWeight: 'bold'}}>
              Sign Up
            </h4>
            <br/><br/><br/>
            <Form onSubmit={this.Signup}>
              <Row>
                <Col style={{paddingLeft: '100px', paddingRight: '100px'}}>
                  <Input style={{border: 'none', borderBottom: '1px solid #1faced', color: '#3360A2', backgroundColor: 'inherit'}} placeholder="Firstname" type="text" name="firstname"
                    value={this.state.firstname} onChange={this.HandleChange} />
                </Col>
              </Row>
              <br/><br/>
              <Row>
                <Col style={{paddingLeft: '100px', paddingRight: '100px'}}>
                  <Input style={{border: 'none', borderBottom: '1px solid #1faced', color: '#3360A2', backgroundColor: 'inherit'}} placeholder="Lastname" type="text" name="lastname"
                    value={this.state.lastname} onChange={this.HandleChange} />
                </Col>
              </Row>
              <br/><br/>
              <Row>
                <Col style={{paddingLeft: '100px', paddingRight: '100px'}}>
                  <Input style={{border: 'none', borderBottom: '1px solid #1faced', color: '#3360A2', backgroundColor: 'inherit'}} placeholder="Username" type="text" name="username"
                    value={this.state.username} onChange={this.HandleChange} />
                </Col>
              </Row>
              <br/><br/>
              <Row>
                <Col style={{paddingLeft: '100px', paddingRight: '100px'}}>
                  <Input style={{border: 'none', borderBottom: '1px solid #1faced', color: '#3360A2', backgroundColor: 'inherit'}} placeholder="Password" type="password" name="password"
                    value={this.state.password} onChange={this.HandleChange} />
                </Col>
              </Row>
              <br/><br/>
              <Button type='submit' style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold', width: '120px'}}>
                Signup
              </Button>
            </Form>
            <br/><br/>
            <a href='/' style={{color: 'inherit'}}>
              Already have an account? Click here to signin.
            </a>
            <br/><br/><br/>
          </Col>
        </Row>
      </div>
    );
  }

};

export default withCookies(Signup);