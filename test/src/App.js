import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';

const API = "http://localhost:8001/lastfm/ooohm"

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: [],
    };
  }

  componentDidMount() {
    fetch(API)
      .then(response => response.json())
      .then(data => this.setState({data: data.topartists.artist}));
  }

  render() {
    const data = this.state.data
    console.log(data)
    return (
    <div>
      <h1>Welcome!</h1>
      <h3>To my test page!</h3>
      <p>Where I will test out my <code>API calls</code> locally.</p>
      <p>I'm new to all this and <i>not very good!</i> So give me some time to <b>learn!</b></p>

      <h3>Top artists of last month:</h3>
      <ol className='artists'>
        {data.map(artist =>
          <li>
            {artist.name} -- {artist.playcount} plays
          </li>
        )}
      </ol>
    </div>
    )
  }
}

export default App;
