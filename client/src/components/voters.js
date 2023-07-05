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

class Voters extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: '',
      loading: false,
      voters: [],
      selected_voter_name: '',
      selected_voter: {}
    };

    this.HandleChange = (e) =>{
      this.setState({[e.target.name]: e.target.value});
    }

    this.SelectVoter = (voter) => {
      this.setState({
        selected_voter_name: voter.firstname + ' ' + voter.lastname,
        selected_voter: voter
      })
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
    var voters = this.state.voters
    var voters_map = this.state.voters.map((item, index) => {
      return<div>
        <Row onClick={() => this.SelectVoter(item)} style={{margin: '0px', cursor: 'pointer'}}>
          <span style={{fontWeight: 'bold'}}>{item.firstname} {item.lastname}</span> | {item.id_number}
        </Row>
        <br/>
      </div>
    })
    var selected_voter = this.state.selected_voter

    return (
      <div>
        <Helmet>
          <title>Voters | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <br/>
        <h4 style={{fontWeight: 'bold'}}>Voters</h4>
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
              <Col sm='4'>
                {
                  voters.length == 0
                  ? <div>
                    <br/><br/><br/>
                    <h5 style={{color: '#1faced'}}>No voters found</h5>
                    <br/><br/><br/>
                    <ThreeDots width='180px' style={{color: '#1faced'}}/>
                  </div>
                  : <div>
                    {voters_map}
                  </div>
                }
              </Col>
              <Col sm='6'>
                {
                  this.state.selected_voter_name == ''
                  ? <div>
                    <br/><br/><br/>
                    <h6 style={{color: '#1faced', fontWeight: 'bold'}}>No voter has been selected yet</h6>
                  </div>
                  : <div>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        Firstname:
                      </Col>
                      <Col>
                        {selected_voter.firstname}
                      </Col>
                    </Row>
                    <br/><br/>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        Lastname:
                      </Col>
                      <Col>
                        {selected_voter.lastname}
                      </Col>
                    </Row>
                    <br/><br/>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        Address:
                      </Col>
                      <Col>
                        {selected_voter.addresss}
                      </Col>
                    </Row>
                    <br/><br/>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        ID Number:
                      </Col>
                      <Col>
                        {selected_voter.id_number}
                      </Col>
                    </Row>
                    <br/><br/>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        Phonenumber:
                      </Col>  
                      <Col>
                        {selected_voter.phonenumber}
                      </Col>
                    </Row>
                    <br/><br/>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        Gender:
                      </Col>
                      <Col>
                        {selected_voter.gender}
                      </Col>
                    </Row>
                    <br/><br/>
                    <Row style={{textAlign: 'left'}}>
                      <Col style={{fontWeight: 'bold'}}>
                        Date of birth:
                      </Col>
                      <Col>
                        {selected_voter.date_of_birth}
                      </Col>
                    </Row>
                    <br/><br/>
                  </div>
                }
              </Col>
            </Row>
          </div>
        }
      </div>
    );
  }

};

export default withCookies(Voters);