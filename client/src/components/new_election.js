import React, { Component, useReducer } from 'react';
import {Collapse, Nav,NavItem,NavLink,UncontrolledDropdown,
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

class NewElection extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: '',
      elections: [],
      loading: false,
      name: '',
      type: '',
      election_date: '',
      contestants: '', // comma separated list
      election_end_date: ''
    };

    this.HandleChange = (e) =>{
      this.setState({[e.target.name]: e.target.value});
    };

    this.SaveElection = () => {
      var name = this.state.name
      var type = this.state.type
      var election_date = this.state.election_date
      var contestants = this.state.contestants
      var election_end_date = this.state.election_end_date

      if (name == ''){
        alert('Name is required')
      }else if (type == ''){
        alert('Type is required')
      }else if (election_date == ''){
        alert('Election date is required')
      }else if (contestants == ''){
        alert('Contestants are required')
      }else if (election_end_date == ''){
        alert('Election end date is required')
      }else{
        this.setState({ loading: true })
        this.state.contract.methods.create(name, type, election_date, contestants, election_end_date).send({ from: this.state.account })
        .once('receipt', (receipt) => {
          alert('Election added successfully')
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
    // get election contract and set to state
    const contract = new web3.eth.Contract(ELECTIONS_ABI, ELECTIONS_ADDRESS)
    this.setState({ contract })
    // get items count and set to state
    const itemsCount = await contract.methods.itemsCount().call()
    this.setState({ itemsCount })
    // populate state with items
    for (var i = 1; i <= itemsCount; i++) {
      const item = await contract.methods.items(i).call()
      // set data to elections state
      this.setState({
        elections: [...this.state.elections, item]
      })
    }
    // stop loading page
    this.setState({loading: false})
  }

  render() {

    return (
      <div>
        <Helmet>
          <title>New Election | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <br/>
        <h4 style={{fontWeight: 'bold'}}>New Election</h4>
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
                  value={this.state.name} placeholder="Election name" type="text" name="name" onChange={this.HandleChange} 
                />
              </Col>
              <Col>
                <Label>Type:</Label>
                <select name='type' value={this.state.type} onChange={this.HandleChange}
                  style={{border: 'none', borderBottom: '1px solid #1faced', width: '100%', backgroundColor: 'inherit', color: '#ffffff', outline: 'none'}}
                >
                  <option>Select election type</option>
                  <option value='Presidential Election'>Presidential Election</option>
                  <option value='Parliamentary Election'>Parliamentary Election</option>
                  <option value='Local Government Election'>Local Government Election</option>
                  <option value='By-Election'>By-Election</option>
                  <option value='Constitutional Referendum'>Constitutional Referendum</option>
                  <option value='Primary Election'>Primary Election</option>
                </select>
              </Col>
            </Row>
            <br/><br/>
            <Row style={{margin: '0px'}}>
              <Col>
                <Label>Election date:</Label>
                <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                  value={this.state.election_date} type="date" name="election_date" onChange={this.HandleChange} 
                />
              </Col>
              <Col>
                <Label>Election end date:</Label>
                <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                  value={this.state.election_end_date} type="date" name="election_end_date" onChange={this.HandleChange} 
                />
              </Col>
            </Row>
            <br/><br/>
            <Row style={{margin: '0px'}}>
              <Col>
                <Label>Contestants:</Label>
                <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}}
                  value={this.state.contestants} placeholder="Contestants (Comma separated name list, eg Contestant 1, Contestant 2, ...)" type="textarea" rows={5} name="contestants" onChange={this.HandleChange} 
                />
              </Col>
              <Col>

              </Col>
            </Row>
            <br/><br/><br/>
            <Button onClick={this.SaveElection} 
              style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold'}}
            >
              Save Election
            </Button>
          </div>
        }
      </div>
    );
  }

};

export default withCookies(NewElection);