package battleships;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Battleships {
	/** Random number generator for our auto play game strategy. */
    static Random r = new Random();

    /* Use this method to define the bot's strategy.
     */
    public static BattleshipsMove calculateMove(MainWindow.GameState state) {
        if(state.Round==0) {
        	return placeShips(state);
        }
        else {
        	return findShips(state);
        }
    }
    
    private static BattleshipsMove placeShips(MainWindow.GameState state) {
    	ArrayList<ShipPosition> placement = new ArrayList<ShipPosition>();
    	int row = 0, column = 0;
    	String orientation = "";
	    for (int i = 0; i < state.Ships.size(); i++) {
	    	boolean placed = false;
	    	while(!placed) {
	    		ArrayList<ArrayList<String>> board = state.MyBoard;
	    		row = r.nextInt(board.size());
	    		column = r.nextInt(board.get(0).size());
	    		String[] orientations = {"H","V"};
	    		orientation = orientations[r.nextInt(2)];
	    		board = attemptShipPlacement(row, column, state.MyBoard, state.Ships.get(i), orientation, i);
	    		if(board != null) {
	    			placed = true;
	    			state.MyBoard = board;
	    		}
	    	}
	    	placement.add(new ShipPosition(Character.toString((char)(row+65)), column+1, orientation));
	    }
	    return new BattleshipsMove(placement, "", 0);
    }
    
    private static BattleshipsMove findShips(MainWindow.GameState state) {
    	boolean placed = false;
		int row=0, column=0;
    	while(!placed) {
    		ArrayList<ArrayList<String>> board = state.MyBoard;
    		row = r.nextInt(board.size());
    		column = r.nextInt(board.get(0).size());
    		if(state.OppBoard.get(row).get(column).equals("") || state.OppBoard.get(row).get(column).equals("L")) {
    			placed = true;
    		}
    	}
    	return new BattleshipsMove(null, Character.toString((char)(row+65)), column+1);
    }
    
    private static ArrayList<ArrayList<String>> attemptShipPlacement(int i, int j, ArrayList<ArrayList<String>> board, int length, String orientation, int shipNum){
    	if(orientation.equals("V")) { //Vertical
    		if(i + length - 1 >= board.size()) { //If ship doesn't fit within board boundaries
    			return null;
    		}
    		for(int l=0; l < length; l++) {
    			String square = board.get(i+l).get(j);
    			if(!square.equals("")) {
    				return null;
    			}
    		}
    		for(int l=0; l < length; l++) {
    			board.get(i+l).set(j, Integer.toString(shipNum));
    		}
    		return board;
    	} else { //Horizontal
    		if(j + length - 1 >= board.get(0).size()) { //If ship doesn't fit within board boundaries
    			return null;
    		}
    		for(int l=0; l < length; l++) {
    			String square = board.get(i).get(j+l);
    			if(!square.equals("")) {
    				return null;
    			}
    		}
    		for(int l=0; l < length; l++) {
    			board.get(i).set(j+l, Integer.toString(shipNum));
    		}
    		return board;
    	}
    }
}