package battleships;

import java.util.ArrayList;

public class BattleshipsMove {
    
    public ArrayList<ShipPosition> Placement = new ArrayList<ShipPosition>();
    public String Row;
    public int Column;
    
    public BattleshipsMove(ArrayList<ShipPosition> placement, String row, int column) {
    	this.Placement = placement;
    	this.Row = row;
    	this.Column = column;
    }
}