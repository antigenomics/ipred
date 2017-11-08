import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.ArrayList;

class Hamming {
  public static void main(String[] args) throws Exception {
    /* Reading the file **/
    String filename = args[0];
    ArrayList<String> lines = new ArrayList<String>();
    try (BufferedReader br = new BufferedReader(new FileReader(filename)))
    {
      String sCurrentLine;
      
      while ((sCurrentLine = br.readLine()) != null) {
        lines.add(sCurrentLine);
      }
    } catch (IOException e) {
            e.printStackTrace();
    }
    
    /* Performing hamming function **/
    for (String line : lines) {
      for (int i=0; i<lines.size(); i++) {
        hamming(line, lines.get(i));
      }
    }
    
  }
  
  public static void hamming (String a, String b) {
    int hamdist = 0;
    for (int i = 0; i<a.length(); i++){
      if (a.charAt(i) != b.charAt(i)) {
        hamdist++;
      }
    }
    if (hamdist<=3){
      System.out.println(a+","+b+","+Integer.toString(hamdist));
    }
  }
}

