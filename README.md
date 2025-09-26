# Web-Security-Tool
Security Script Programming - Project using Python

Run the API first then test using these values:

SQL-like (target name/email)
<br/>
  • name: Robert'); DROP TABLE users;--                     <br/>
  • name: ' OR '1'='1                                       <br/>
  • email: attacker@example.com'; DROP TABLE users;--       <br/>
  • email: not-an-email                                     <br/>

XSS test
<br/>
  • name: <script>alert('xss')</script>
  <br/>
  • email: user@example.com<script>
  <br/>
  • message: <script>alert('hack')</script>

Age tests
<br/>
  • age: ""     # optional -> allowed
  <br/>
  • age: 25     # valid
  <br/>
  • age: 5      # invalid range
  <br/>
  • age: abc    # invalid number

Message tests
<br/>
  • message: https://www.python.org           # valid URL
  <br/>
  • message: Robert'); DROP TABLE users;--    # invalid URL
  <br/>
  • message: javascript:alert('xss')          # JS injection attempt
  <br/>
  • message: Hello, this is just text         # plain text
