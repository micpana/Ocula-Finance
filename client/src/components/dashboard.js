import React, { Component, useReducer } from 'react';
import {Collapse, Nav,NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Form, Container, Label, InputGroup} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import {Helmet} from 'react-helmet'
import Logo from '../images/logos/logo.png'
import {CgAppleWatch, CgChart, CgImport} from 'react-icons/cg'
import {AiFillCheckCircle, AiOutlineAreaChart, AiOutlineBook, AiOutlineLineChart, AiOutlineSetting} from 'react-icons/ai'
import {CgNotes} from 'react-icons/cg'
import {BiUserCircle} from 'react-icons/bi'
import {FaEdit, FaNewspaper, FaRegMoneyBillAlt, FaUsers} from 'react-icons/fa'
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
import RegisterVoter from './register_voter'
import Voters from './voters'
import NewElection from './new_election'
import Vote from './vote'
import ElectionResults from './election_results'
import Web3 from 'web3'
import {Blockchain_Address} from '../blockchain_address'
import { VOTERS_ABI, VOTERS_ADDRESS, ELECTIONS_ABI, ELECTIONS_ADDRESS, VOTES_ABI, VOTES_ADDRESS, STAFF_ABI, STAFF_ADDRESS } from '../config'

class Dashboard extends Component{
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };
  constructor(props) { 
    super(props);
    this.state = {
      account: '',
      staff: [],
      current_view: 'welcome',
      dropdownOpen: false,
      loading: false
    };

    this.Signout = () =>{
      const { cookies } = this.props;
      cookies.remove('token', { path: '/' });
    };

    this.dtoggle = () => {
      this.setState(prevState => ({
        dropdownOpen2: !prevState.dropdownOpen
      }));
    }

    this.onMouseEnter = () => {
      this.setState({dropdownOpen: true});
    };

    this.onMouseLeave = () => {
      this.setState({dropdownOpen: false});
    };

    this.HandleChange = (e) =>{
      this.setState({[e.target.name]: e.target.value});
    };

    this.ChangeView = (selected_view) => {
      document.getElementById(this.state.current_view).style.color = '#ffffff'
      document.getElementById(selected_view).style.color = 'black'

      this.setState({current_view: selected_view})
    }

    this.CurrentView = () => {
      var current_view = this.state.current_view

      if(current_view == 'welcome'){
        var d = new Date();
        var time = d.getHours();
        var greeting = ''

        if (time < 12) {
          greeting = 'Good morning'
        }
        if (time >= 12 && time < 18) {
          greeting = 'Good afternoon'
        }
        if (time >= 18) {
          greeting = 'Good evening'
        }

        return <div>
          <Helmet>
            <title>Welcome | E-Voting</title>
            {/* <meta name="description" content="" /> */}
          </Helmet>
              <br/><br/><br/><br/>
              <h2 id='welcome' style={{color: '#1faced'}}>{greeting} {this.state.user_details.firstname}!</h2>
              <br/><br/><br/>
              <Circles width='180px' style={{color: '#1faced'}}/>
        </div>
      }else if(current_view == 'register_voters'){
        return <RegisterVoter ChangeView={this.ChangeView}/>
      }else if(current_view == 'voters'){
        return <Voters ChangeView={this.ChangeView}/>
      }else if(current_view == 'new_election'){
        return <NewElection ChangeView={this.ChangeView} />
      }else if(current_view == 'vote'){
        return <Vote ChangeView={this.ChangeView} />
      }else if(current_view == 'election_results'){
        return <ElectionResults ChangeView={this.ChangeView} />
      }else{
        return<div>
          <br/><br/>
          Something went wrong, please try again or reload the web page.
        </div>
      }
    }
  }

  componentDidMount() {
    // document.getElementById(this.state.current_view).style.color = '#1faced'

    const { cookies } = this.props;
    if(cookies.get('token')==null){
      let port = (window.location.port ? ':' + window.location.port : '');
      window.location.href = '//' + window.location.hostname + port + '/';
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
    const { cookies } = this.props;
    var user_details = {}
    var matches = this.state.staff.filter(item => item.id == cookies.get('token'))
    if (matches.length > 0){
      user_details = matches[0]
    }

    return (
      <div>
        <Helmet>
          <title>Dashboard | E-Voting</title>
          {/* <meta name="description" content="" /> */}
        </Helmet>
        <Row style={{marginRight: '0px'}}>
          <Col sm='2' style={{minHeight: '630px', backgroundColor: '#237fa0', color: '#ffffff', textAlign: 'left'}}>
            <Container style={{textAlign: 'left'}}>
              <br/>
              E-Voting
              <div style={{border: '1px solid #ffffff', marginTop: '5px'}}></div>
              <br/>
            </Container>
            <br/><br/>
            <Button id='register_voter' onClick={() => this.ChangeView('register_voter')} style={{textAlign: 'left', width: '100%', border: 'none', backgroundColor: 'inherit', color: 'inherit', outline: 'none', boxShadow: 'none'}}>
              <FaEdit /> Register Voter
            </Button>
            <br/><br/>
            <Button id='voters' onClick={() => this.ChangeView('voters')} style={{textAlign: 'left', width: '100%', border: 'none', backgroundColor: 'inherit', color: 'inherit', outline: 'none', boxShadow: 'none'}}>
              <FaUsers /> Voters
            </Button>
            <br/><br/>
            <Button id='new_election' onClick={() => this.ChangeView('new_election')} style={{textAlign: 'left', width: '100%', border: 'none', backgroundColor: 'inherit', color: 'inherit', outline: 'none', boxShadow: 'none'}}>
              <FaNewspaper /> New Election
            </Button>
            <br/><br/>
            <Button id='vote' onClick={() => this.ChangeView('vote')} style={{textAlign: 'left', width: '100%', border: 'none', backgroundColor: 'inherit', color: 'inherit', outline: 'none', boxShadow: 'none'}}>
              <AiFillCheckCircle /> Vote
            </Button>
            <br/><br/>
            <Button id='election_results' onClick={() => this.ChangeView('election_results')} style={{textAlign: 'left', width: '100%', border: 'none', backgroundColor: 'inherit', color: 'inherit', outline: 'none', boxShadow: 'none'}}>
              <AiOutlineBook /> Election Results
            </Button>
            <br/><br/>
          </Col>
          <Col>
            <Row style={{marginRight: '0px', backgroundColor: '#1faced', height: '60px', marginTop: '10px'}}>
              <Container style={{textAlign: 'right'}}>
                  <Dropdown className="d-inline-block" onMouseOver={this.onMouseEnter} onMouseLeave={this.onMouseLeave} isOpen={this.state.dropdownOpen} toggle={this.dtoggle}>
                    <DropdownToggle  style={{marginTop: '', backgroundColor:  'inherit', border: 'none', fontSize: '10px', color: '#ffffff'}}>
                      <BiUserCircle size='25px'/>
                      <br/>
                      <span style={{fontWeight: 'bold'}}>
                        {user_details.firstname} {user_details.lastname}
                      </span>
                    </DropdownToggle>
                    <DropdownMenu>
                      <DropdownItem  onClick={this.Signout}>
                          <NavLink style={{color: '#F0453A', backgoundColor: 'inherit'}} >
                              Signout
                          </NavLink>
                      </DropdownItem>
                    </DropdownMenu>
                  </Dropdown>
              </Container>
            </Row>
            <Row style={{marginRight: '0px'}}>
              <Container>
                  <this.CurrentView/>
                  <br/><br/><br/>
              </Container>
            </Row>
          </Col>
        </Row>
      </div>
    );
  }

};

export default withCookies(Dashboard);