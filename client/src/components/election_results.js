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

class LiveElectionResults extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: '',
      loading: false,
      votes: [],
      past_elections: [],
      selected_election: {},
      current_view: 'elections' // elections / election
    };

    this.HandleChange = (e) => {
      this.setState({[e.target.name]: e.target.value});
    };

    this.SelectElection = (election) => {
      this.setState({
        selected_election: election,
        current_view: 'election'
      })
    }
  }

  componentDidMount() {

  }
  
  componentWillMount() {
    this.loadVotesBlockchainData()
    this.loadElectionsBlockchainData()
  }

  async loadVotesBlockchainData() {
    // load page
    this.setState({loading: true})
    // connect to the blockchain
    const web3 = new Web3(Blockchain_Address)
    // get account information
    const accounts = await web3.eth.getAccounts()
    this.setState({ account: accounts[0] })
    console.log('List of accounts:', accounts)
    // get votes contract and set to state
    const contract = new web3.eth.Contract(VOTES_ABI, VOTES_ADDRESS)
    const contract1 = contract
    this.setState({ contract1 })
    // get items count and set to state
    const itemsCount = await contract.methods.itemsCount().call()
    const itemsCount1 = itemsCount
    this.setState({ itemsCount1 })
    // populate state with items
    for (var i = 1; i <= itemsCount; i++) {
      const item = await contract.methods.items(i).call()
      // set data to votes state
      this.setState({
        votes: [...this.state.votes, item]
      })
    }
    // stop loading page
    this.setState({loading: false})
  }

  async loadElectionsBlockchainData() {
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
    const contract2 = contract
    this.setState({ contract2 })
    // get items count and set to state
    const itemsCount = await contract.methods.itemsCount().call()
    const itemsCount2 = itemsCount
    this.setState({ itemsCount2 })
    // populate state with items
    for (var i = 1; i <= itemsCount; i++) {
      const item = await contract.methods.items(i).call()
      // get current date
      let date = new Date();
      date.setHours(0, 0, 0, 0); // set hours, minutes, seconds, and milliseconds all to 0
      let formatted_current_date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
      console.log('current data:', formatted_current_date);
      // check if election is a past election
      if (item.election_end_date > formatted_current_date){
        // set data to elections state
        this.setState({
          past_elections: [...this.state.past_elections, item]
        })
      }
    }
    // stop loading page
    this.setState({loading: false})
  }

  render() {
    var past_elections = this.state.past_elections
    var elections_map = past_elections.map((item, index) => {
      return <div>
        <Row onClick={() => this.SelectElection(item)} style={{margin: '0px', cursor: 'pointer'}}>
          {item.name} | from {item.election_date} to {item.election_end_date} | {item.typee}
        </Row>
        <br/><br/>
      </div>
    })
    var selected_election = this.state.selected_election
    var votes = this.state.votes

    return (
      <div>
        <Helmet>
          <title>Live Election Results | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <br/>
        <h4 style={{fontWeight: 'bold'}}>Election Results</h4>
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
            {
              this.state.current_view == 'elections'
              ? <div>
                {
                  past_elections.length == 0
                  ? <div>
                    <br/><br/><br/>
                    <h6 style={{color: '#1faced'}}>No past elections found</h6>
                    <br/><br/><br/>
                    <ThreeDots width='70px' style={{color: '#1faced'}}/>
                  </div>
                  : <div>
                    {elections_map}
                  </div>
                }
              </div>
              : <div> {/* election */}
                <Button onClick={() => this.setState({current_view: 'elections'})} 
                  style={{backgroundColor: 'inherit', color: '#1faced', border: 'none', borderRadius: '20px', fontWeight: 'bold'}}
                >
                  {'<<<'} Past election list
                </Button>
                <br/><br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                  <Col>
                    <Label style={{fontWeight: 'bold'}}>Name:</Label>
                    {selected_election.name}
                  </Col>
                  <Col>
                    <Label style={{fontWeight: 'bold'}}>Type:</Label>
                    {selected_election.typee}
                  </Col>
                  <Col>
                    <Label style={{fontWeight: 'bold'}}>Election date:</Label>
                    {selected_election.election_date}
                  </Col>
                  <Col>
                    <Label style={{fontWeight: 'bold'}}>Election end date:</Label>
                    {selected_election.election_end_date}
                  </Col>
                </Row>
                <br/><br/>
                <h6 style={{fontWeight: 'bold'}}>
                  Contestants and their received votes:
                </h6>
                <br/>
                {
                  selected_election.contestants.split(',').map((item) => {
                    return<div>
                      <Row style={{margin: '0px', textAlign: 'left'}}
                      >
                        <Col>
                          {item}
                        </Col>
                        <Col>
                          {votes.filter(i => i.contestant == item && i.election_id == selected_election.id).length}
                        </Col>
                      </Row>
                      <br/>
                    </div>
                  })
                }
              </div>
            }
          </div>
        }
      </div>
    );
  }

};

export default withCookies(LiveElectionResults);