<!DOCTYPE html>
<html>
<body>
<p>IP: {{ !ipaddress }}</p>
<form action='/account' method='post'> 
<p>Όνομα: <input name='username' type='text' value='{{!username}}'/></p>
<p>Ομάδα:  <input type="radio" name="team" value="blue" {{!checkedBlue}}>Μπλε<input type="radio" name="team" value="red" {{!checkedRed}}>Κόκκινη</p>
<p><input type="checkbox" name="spymaster" value="true" {{spymaster}}>Αρχικατάσκοπος</label><p>
<p><input value='Αποθήκευση' type='submit' /></p></form>
</body>
</html>