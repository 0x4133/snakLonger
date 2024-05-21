# Load .NET assemblies for input simulation
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class User32 {
    [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true)]
    public static extern void mouse_event(int dwFlags, int dx, int dy, int cButtons, int dwExtraInfo);
    public const int MOUSEEVENTF_LEFTDOWN = 0x02;
    public const int MOUSEEVENTF_LEFTUP = 0x04;

    [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true)]
    public static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
    public const int KEYEVENTF_KEYUP = 0x02;
}

public class InputSimulator {
    public static void ClickAt(int x, int y) {
        Cursor.Position = new System.Drawing.Point(x, y);
        User32.mouse_event(User32.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        User32.mouse_event(User32.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }

    public static void TypeText(string text) {
        foreach (char c in text) {
            short vk = (short)System.Windows.Forms.Keys.GetValue(c.ToString().ToUpper());
            User32.keybd_event((byte)vk, 0, 0, 0);
            User32.keybd_event((byte)vk, 0, User32.KEYEVENTF_KEYUP, 0);
        }
    }
}
"@

# Function to click at specified coordinates
function Click-At($x, $y) {
    [InputSimulator]::ClickAt($x, $y)
}

# Function to type specified text
function Type-Text($text) {
    [InputSimulator]::TypeText($text)
}

# Example usage
# Click at (100, 200), wait for 1 second, then type "Hello"
Click-At -x 100 -y 200
Start-Sleep -Seconds 1
Type-Text -text "Hello"

# Add additional clicks and text typing as needed
Click-At -x 150 -y 250
Start-Sleep -Seconds 1
Type-Text -text "World"