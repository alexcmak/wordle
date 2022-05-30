import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Wordle {

    private enum GuessResult { EXACT_CORRECT, APPEAR_WRONG_POSITION, NOT_APPEAR_AT_ALL}
    private final static int MAX=5;
    private final static int MAX_TRIALS=6;

    List<String> fiveletterwords = new ArrayList<String>();

    public static void main(String arg[]) {

       Wordle me = new Wordle();
       me.readWordList("words5.txt");
       try {
           String guessWord = me.getGuessWord();
           me.runGame(guessWord);
       } catch (Exception e) {
           e.printStackTrace();
       }
    }

    public void readWordList(String wordListFilePath) {
        Scanner myReader = null;
        try {
            File myObj = new File(wordListFilePath);
             myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                fiveletterwords.add((String)data);
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.err.println("An error occurred trying to read "+wordListFilePath);
            e.printStackTrace();
        }
        finally {
            if (myReader!=null) myReader.close();
        }
    }

    public String getGuessWord() {
        int random_int = (int)Math.floor(Math.random()*(fiveletterwords.size()+1));

        return (String) fiveletterwords.get(random_int);
        //return "games";
    }

    public boolean isWordInList(String word) {
        return fiveletterwords.contains(word);
        //return true;
    }

    public String readWordFromUser(BufferedReader bf) throws Exception  {

        boolean isValidWord = false;
        String str="";
        while (!isValidWord) {
            System.out.print("Please enter a "+MAX+" letter word:");
            str = bf.readLine();
            //System.out.println("You entered: " + str);

            if (str.length() != MAX) {
                System.out.println("You must enter a "+MAX+" letter word");
                continue;

            }
            else
            if (!isWordInList(str)) {
                System.out.println("You must enter a valid "+MAX+" letter word");
                continue;
            }

            isValidWord=true;
        }
        return str;
    }

    private void showGuessResult(String choice,GuessResult guessResult[]) {
        for (int i=0; i < MAX; i++) {
            String color="";
            switch (guessResult[i]) {
                case EXACT_CORRECT: color="GREEN"; break;
                case APPEAR_WRONG_POSITION: color="ORANGE"; break;
                case NOT_APPEAR_AT_ALL: color="GREY"; break;
            }
            System.out.println(choice.charAt(i)+":"+color);
        }

    }

    public GuessResult[] evaluateGuess(String wordToGuess, String userGuess) {
        GuessResult result[] = new GuessResult[MAX];
        char[] guessWordArray = wordToGuess.toCharArray();

        for (int i=0; i < MAX; i++) {
            if (guessWordArray[i] == userGuess.charAt(i)) {
                result[i] = GuessResult.EXACT_CORRECT;
                guessWordArray[i]=' ';
            }
        }

        for (int i=0; i < MAX; i++) {
            //System.out.println("i="+i);

            if (result[i] == GuessResult.EXACT_CORRECT) continue;

            boolean found=false;
            for (int j=0; j < MAX; j++) {
                //System.out.println("comparing "+choice.charAt(i)+" vs "+guessWordArray[j]);
                if (userGuess.charAt(i)==guessWordArray[j]) {
                    result[i]=GuessResult.APPEAR_WRONG_POSITION;
                    guessWordArray[j]=' ';
                    found=true;
                    break;
                }
            }

            if (!found) {
                //System.out.println( choice.charAt(i)+": GRAY");
                result[i]=GuessResult.NOT_APPEAR_AT_ALL;
            }
        }
        return result;
    }

    public void runGame(String guessWord) throws Exception {

        BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
        boolean gameOver = false;
        int trial=1;

        while (!gameOver) {
            System.out.println("Trial "+trial);
            //System.out.println("shh, it is: "+guessWord);

            String choice = readWordFromUser(bf);

            if (choice.equals(guessWord)) {
                System.out.println("You won!");
                break;
            }

            GuessResult guessResult[] = evaluateGuess(guessWord, choice);

            showGuessResult(choice,guessResult);

            trial++;
            if (trial>MAX_TRIALS) {
                System.out.println("Sorry you lost, the word is: "+guessWord);
                gameOver=true;
            }
        }
        bf.close();

    }
}

