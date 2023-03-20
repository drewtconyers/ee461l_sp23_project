import './App.css';

function App() {
  return (
    <div style={{ justifyContent: 'center' }}><center>
    <h1>Login Page</h1>
    <table>
        <tr>
            <td>User ID:</td>
            <td>
                <input type="text" name="userID"></input>
            </td>
        </tr>
        <tr>
            <td>Password:</td>
            <td>
                <input type="password" name="password"></input>
            </td>
        </tr>
        <tr>
            <td>
                <input type="submit" name="submit" value="login"></input>
            </td>
        </tr>
    </table>
    <a href="{{url_for('register')}}">Register Here</a>
    </center>
</div>
  );
}

export default App;
