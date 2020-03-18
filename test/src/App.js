import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';

const API = "http://localhost:8001/lastfm/"

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      user: 'ooohm',
      artists: [],
    };

    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange(event) {
    this.setState({user: event.target.value.toLowerCase()});

  }

  handleSubmit(event) {
    alert("Getting top artists for: " + this.state.user);
    this.componentDidMount()
    event.preventDefault();
  }

  componentDidMount() {
    console.log(this.state.artists);
    fetch(API+this.state.user)
      .then(response => response.json())
      .then(data => this.setState({artists: data.topartists.artist}));
  }

  render() {
    const artists = this.state.artists
    console.log(artists)
    return (
    <div className="App">
      <h1>API Test page</h1>
      <h3>Last.fm api test page</h3>
      <p>Where I will test out my <code>API calls</code> locally.</p>
      <p>I'm new to all this and <i>not very good!</i> So give me some time to <b>learn!</b></p>
      <p>Currently, React fetches from a FastAPI backend which itself fetches from Last.fm.</p>
      <h3>Enter username:</h3>
      <form onSubmit={this.handleSubmit}>
        <label>
          Username:
          <input type="text" value={this.state.user} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      <h3>Top artists of last month:</h3>
      <ol className='artists'>
        {artists.map(artist =>
        <li className='artistEntry'>
            <p><a href={artist.url}>{artist.name}</a> -- {artist.playcount} plays</p>
          </li>
        )}
      </ol>
    </div>
    )
  }
}

export default App;
