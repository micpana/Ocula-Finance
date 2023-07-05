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

class Election extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      loading: false,
      votes: [],
      active_elections: [],
      voters: [],
      voting_voter: {},
      selected_election: {},
      current_view: 'election_list' // election_list / vote
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

    this.CreateVoterSignature = (voter) => {
      var signature = null

      // return signature
      return signature
    }

    this.Vote = (election, contestant) => {
      var proceed = confirm('You have selected ' + contestant + ' as your candidate choice. Press "OK" to continue.')
      if (proceed == true){
        // verify identity ... request fullname and id number via prompts
        var fullname = prompt('Enter your firstname and lastname as on your National ID Card')
        var id_number = prompt('Enter your ID number as on your National ID Card')
        var voter_matches = this.state.voters.filter(item => // look for name + id number match
          fullname.toUpperCase() == item.firstname.toUpperCase() + ' ' + item.lastname.toUpperCase() && 
          id_number.toUpperCase().replace('-', '') == item.id_number.toUpperCase().replace('-', '')
        )
        if (voter_matches.length == 0){
          alert('No registered voter with entered details found. Please make sure you are a registered voter and you have entered your details correctly.')
        }else{
          var voter = voter_matches[0]
          this.setState({voting_voter: voter})
          // create signature
          var voter_signature = this.CreateVoterSignature(voter)
          // check if voter hasn't voted on this election already
          var vote_matches = this.state.votes.filter(item => // look for election_id + voter_signature matches
            item.election_id == election.id &&
            item.signature == voter_signature
          )
          if (vote_matches.length > 0){
            alert('You have already voted in this election. Please note that you can only cast your vote once.')
          }else{
            // cast vote
            this.setState({ loading: true })
            this.state.contract1.methods.create(election.id, contestant, voter_signature).send({ from: this.state.account })
            .once('receipt', (receipt) => {
              // reload data
              this.loadVotesBlockchainData()
              this.loadElectionsBlockchainData()
              this.loadVotersBlockchainData()
              alert('Vote casted successfully.')
              this.setState({ 
                voting_voter: {},
                selected_election: {},
                current_view: 'election_list',
                loading: false 
              })
            })
          }
        }
      }else{
        alert('Candidate selection cancelled.')
      }
    }
  }

  componentDidMount() {
    
  }
  
  componentWillMount() {
    this.loadVotesBlockchainData()
    this.loadElectionsBlockchainData()
    this.loadVotersBlockchainData()
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
      // check if election is an active election
      if (formatted_current_date >= item.election_date && formatted_current_date <= item.election_end_date){
        // set data to elections state
        this.setState({
          active_elections: [...this.state.active_elections, item]
        })
      }
    }
    // stop loading page
    this.setState({loading: false})
  }

  async loadVotersBlockchainData() {
    // load page
    this.setState({loading: true})
    // connect to the blockchain
    const web3 = new Web3(Blockchain_Address)
    // get account information
    const accounts = await web3.eth.getAccounts()
    this.setState({ account: accounts[0] })
    console.log('List of accounts:', accounts)
    // get votes contract and set to state
    const contract = new web3.eth.Contract(VOTERS_ABI, VOTERS_ADDRESS)
    const contract3 = contract
    this.setState({ contract3 })
    // get items count and set to state
    const itemsCount = await contract.methods.itemsCount().call()
    const itemsCount3 = itemsCount
    this.setState({ itemsCount3 })
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
    var elections = this.state.active_elections
    var elections_map = elections.map((item, index) => {
      return <div>
        <Row onClick={() => this.SelectElection(item)} style={{margin: '0px', cursor: 'pointer'}}>
          {item.name} | from {item.election_date} to {item.election_end_date} | {item.typee}
        </Row>
        <br/><br/>
      </div>
    })
    var selected_election = this.state.selected_election

    return (
      <div>
        <Helmet>
          <title>Vote | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <br/>
        <h4 style={{fontWeight: 'bold'}}>Vote</h4>
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
              this.state.current_view == 'election_list'
              ? <div>
                {elections_map}
              </div>
              : <div> {/* vote */}
                <Button onClick={() => this.setState({current_view: 'election_list'})} 
                  style={{backgroundColor: 'inherit', color: '#1faced', border: 'none', borderRadius: '20px', fontWeight: 'bold'}}
                >
                  {'<<<'} Active election list
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
                  Contestants:
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
                          <Button onClick={() => this.Vote(selected_election, item)} 
                            style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold'}}
                          >
                            Cast here
                          </Button>
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

export default withCookies(Election);