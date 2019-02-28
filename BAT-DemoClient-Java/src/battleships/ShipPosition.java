package battleships;

public class ShipPosition {

    public String Row;
    public int Column;
    public String Orientation;
    
    public ShipPosition(String row, int column, String orientation) {
    	this.Orientation = orientation;
    	this.Row = row;
    	this.Column = column;
    }
}