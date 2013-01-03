import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.junit.Test;
import static org.junit.Assert.*;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import org.junit.runner.Description;
import org.junit.runner.notification.RunListener;

public class LinkedListTest {
    @Test 
    public void testExistence() {
	int expected = 2;
	int result = 4;
	assertTrue("WTF mate", expected == result);
    }

    @Test 
    public void testHappy() {
	int expected = 2;
	int result = 4;
	assertFalse("WTF mate", expected == result);
    }

    public static void main(String[] args) {
	System.out.println("Starting...");
	JUnitCore core= new JUnitCore();
	core.addListener(new RetroPrinter());
	core.run(LinkedListTest.class);
	//	Result result = JUnitCore.runClasses(LinkedListTest.class);
	// for (Failure failure : result.getFailures()) {
	//     System.out.println("Failure: " + failure.getMessage());
	//     Description d = failure.getDescription();
	//     System.out.println("\t" + d.getMethodName());
	// }
	System.out.println("... Ending.");
    }
}
