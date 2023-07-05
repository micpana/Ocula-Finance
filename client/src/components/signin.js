import React, { Component, useReducer } from 'react';
import {Collapse,Navbar,NavbarToggler,NavbarBrand,Nav,NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Table, Form, FormGroup, Container, Label, InputGroup} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import {Helmet} from 'react-helmet'
import SigninImage from '../images/signin.png'
import Web3 from 'web3'
import {Blockchain_Address} from '../blockchain_address'
import { VOTERS_ABI, VOTERS_ADDRESS, ELECTIONS_ABI, ELECTIONS_ADDRESS, VOTES_ABI, VOTES_ADDRESS, STAFF_ABI, STAFF_ADDRESS } from '../config'

class Signin extends Component{
    static propTypes = {
      cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
      super(props);
      this.state = {
        account: '',
        staff: [],
        username: '',
        password: ''
    };

    this.SignIn = (e) => {
      e.preventDefault()
      const { cookies } = this.props
      var username = this.state.username
      var password = this.state.password

      if (username == ''){
        alert('Username is required')
      }else if (password == ''){
        alert('Password is required')
      }else{
        var staff = this.state.staff
        var matches = staff.filter(item => (item.username == username && item.password == password))
        if (matches.length == 0){
          alert('Incorrect details entered')
        }else{
          alert('Signin successful')
          cookies.set('token', matches[0].id, { path: '/' })
          let port = (window.location.port ? ':' + window.location.port : '')
          window.location.href = '//' + window.location.hostname + port + '/dashboard'
        }
      }
    }

    ///////////handle text fields change
    this.HandleChange = (e) =>{
        this.setState({[e.target.name]: e.target.value});
    };//////handle change ends here
  }

  componentDidMount() {
    const { cookies } = this.props;
    if(cookies.get('token')!=null){
      let port = (window.location.port ? ':' + window.location.port : '');
      window.location.href = '//' + window.location.hostname + port + '/dashboard';
    };
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
      <div style={{minHeight: '630px'}}>
        <Helmet>
          <title>Sign In | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <Row style={{margin: '0px'}}>
          <Col style={{backgroundColor: '#ffffff', minHeight: '630px'}}>
            <br/><br/>
            <img src={SigninImage} style={{width: '70%'}} />
          </Col>
          <Col sm='5'>
          <Form onSubmit={this.SignIn} >
            <Container style={{paddingRight: '100px', paddingLeft: '100px'}}>
              <br/><br/><br/><br/><br/><br/>
              <Row>
                <Col>
                  <h4 style={{color: '#1faced', fontWeight: 'bold'}}>Sign In</h4>
                </Col>
              </Row>
              <br/><br/>
              <Row>
                <Col>
                  <InputGroup>
                    <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}} placeholder="Username" type="text" name="username"
                    value={this.state.username} onChange={this.HandleChange} />
                  </InputGroup> 
                </Col>
              </Row>
              <br/><br/>
              <Row>
                <Col>
                  <InputGroup>
                    <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}} placeholder="Password" type="password" name="password"
                    value={this.state.password} onChange={this.HandleChange} />
                  </InputGroup> 
                </Col>
              </Row>
              <br/><br/><br/><br/>
              <Button type="submit" style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold', width: '120px'}}>SignIn</Button>
              <br/><br/><br/>
              <a href='/signup' style={{color: 'inherit'}}>
                Not yet registered? Click here to signup.
              </a>
            </Container>
            </Form>
          </Col>
        </Row>
      </div>
    );
  }

};

export default withCookies(Signin);