package frontend;

import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.*;
import javax.swing.*;
import javax.swing.JFrame;
import javax.swing.WindowConstants;
import javax.swing.JTextField;

public class Display extends JFrame {
	
	Container container;
	container = getContentPane();

	JFrame frame = new JFrame("FrameDemo");
	frame.setSize(300, 400);
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	frame.pack();
	frame.setVisible(true);

	JTextField field = new JTextField(10);
	container.add(field, BorderLayout.SOUTH);
}
}
