import React, { Component, useReducer } from 'react';
import {Collapse, NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Form, Container, Label, InputGroup} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import {Helmet} from 'react-helmet'
import {
  Audio,
  BallTriangle,
  Bars,
  Circles,
  Grid,
  Hearts,
  Oval,
  Puff,
  Rings,
  SpinningCircles,
  TailSpin,
  ThreeDots,
} from '@agney/react-loading';
import Web3 from 'web3'
import {Blockchain_Address} from '../blockchain_address'
import { VOTERS_ABI, VOTERS_ADDRESS, ELECTIONS_ABI, ELECTIONS_ADDRESS, VOTES_ABI, VOTES_ADDRESS, STAFF_ABI, STAFF_ADDRESS } from '../config'

class RegisterVoter extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: '',
      voters: [],
      loading: false,
      firstname: '',
      lastname: '',
      address: '',
      id_number: '',
      phonenumber: '',
      gender: '',
      date_of_birth: ''
    };

    this.HandleChange = (e) =>{
      this.setState({[e.target.name]: e.target.value});
    };

    this.Register = () => {
      var firstname = this.state.firstname
      var lastname = this.state.lastname
      var address = this.state.address
      var id_number = this.state.id_number
      var phonenumber = this.state.phonenumber
      var gender = this.state.gender
      var date_of_birth = this.state.date_of_birth
      var id_number_matches = this.state.voters.filter(item => item.id_number.toLowerCase().replace('-', '') == id_number.toLowerCase().replace('-', ''))

      if (firstname == ''){
        alert('Firstname is required')
      }else if (lastname == ''){
        alert('Lastname is required')
      }else if (address == ''){
        alert('Address is required')
      }else if (id_number == ''){
        alert('ID number is required')
      }else if (id_number_matches.length > 0){
        alert('A registered voter with this ID number already exists')
      }else if (phonenumber == ''){
        alert('Phonenumber is required')
      }else if (gender == ''){
        alert('Gender is required')
      }else if (date_of_birth == ''){
        alert('Date of birth is required')
      }else{
        this.setState({ loading: true })
        this.state.contract.methods.create(firstname, lastname, address, id_number, phonenumber, gender, date_of_birth).send({ from: this.state.account })
        .once('receipt', (receipt) => {
          alert('Voter registered successfully')
          this.setState({ loading: false })
          window.location.reload()
        })
      }
    }
  }

  componentDidMount() {
    
  }
  
  componentWillMount() {
    this.loadBlockchainData()
  }

  async loadBlockchainData() {
    // load page
    this.setState({loading: true})
    // connect to the blockchain
    const web3 = new Web3(Blockchain_Address)
    // get account information
    const accounts = await web3.eth.getAccounts()
    this.setState({ account: accounts[0] })
    console.log('List of accounts:', accounts)
    // get voter contract and set to state
    const contract = new web3.eth.Contract(VOTERS_ABI, VOTERS_ADDRESS)
    this.setState({ contract })
    // get items count and set to state
    const itemsCount = await contract.methods.itemsCount().call()
    this.setState({ itemsCount })
    // populate state with items
    for (var i = 1; i <= itemsCount; i++) {
      const item = await contract.methods.items(i).call()
      // set data to voters state
      this.setState({
        voters: [...this.state.voters, item]
      })
    }
    // stop loading page
    this.setState({loading: false})
  }

  render() {

    return (
      <div>
        <Helmet>
          <title>Register Voters | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <br/>
        <h4 style={{fontWeight: 'bold'}}>Register Voter</h4>
        <br/><br/>
        {
            this.state.loading == true
            ? <div>
                <br/><br/><br/>
                <h5 style={{color: '#1faced'}}>Loading...</h5>
                <br/><br/><br/>
                <Oval width='180px' style={{color: '#1faced'}}/>
            </div>
            : <div>
              <Row style={{margin: '0px'}}>
                <Col>
                  <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                    value={this.state.firstname} placeholder="Firstname" type="text" name="firstname" onChange={this.HandleChange} 
                  />
                </Col>
                <Col>
                  <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                    value={this.state.lastname} placeholder="Lastname" type="text" name="lastname" onChange={this.HandleChange} 
                  />
                </Col>
              </Row>
              <br/><br/>
              <Row style={{margin: '0px'}}>
                <Col>
                  <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                    value={this.state.address} placeholder="Address" type="text" name="address" onChange={this.HandleChange} 
                  />
                </Col>
                <Col>
                  <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                    value={this.state.id_number} placeholder="ID number" type="text" name="id_number" onChange={this.HandleChange} 
                  />
                </Col>
              </Row>
              <br/><br/>
              <Row style={{margin: '0px'}}>
                <Col>
                  <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                    value={this.state.phonenumber} placeholder="Phonenumber" type="text" name="phonenumber" onChange={this.HandleChange} 
                  />
                </Col>
                <Col>
                  <Label>Gender:</Label>
                  <select name='gender' value={this.state.gender} onChange={this.HandleChange}
                    style={{border: 'none', borderBottom: '1px solid #1faced', width: '100%', backgroundColor: 'inherit', color: '#ffffff', outline: 'none'}}
                  >
                    <option>Select gender</option>
                    <option value='Male'>Male</option>
                    <option value='Female'>Female</option>
                  </select>
                </Col>
              </Row>
              <br/><br/>
              <Row style={{margin: '0px'}}>
                <Col>
                  <Label>Date of birth:</Label>
                  <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                    value={this.state.date_of_birth} type="date" name="date_of_birth" onChange={this.HandleChange} 
                  />
                </Col>
                <Col>

                </Col>
              </Row>
              <br/><br/><br/>
              <Button onClick={this.Register} 
                style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold'}}
              >
                Register Voter
              </Button>
            </div>
        }
      </div>
    );
  }

};

export default withCookies(RegisterVoter);