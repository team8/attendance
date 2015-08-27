package backend;

import java.sql.*;
import java.math.*;

public class DatabaseConnection {

	public void registerDriver() {
		
		try {
			   Driver myDriver = new oracle.jdbc.driver.OracleDriver();
			   DriverManager.registerDriver( myDriver );
			}
			catch(ClassNotFoundException ex) {
			   System.out.println("Error: unable to load driver class!");
			   System.exit(1);
			}
	}
	
	
}
