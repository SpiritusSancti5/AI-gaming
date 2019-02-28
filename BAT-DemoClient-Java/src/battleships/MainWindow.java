package battleships;

import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.List;
import java.util.Random;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.awt.Component;
import java.awt.Dimension;
import java.util.ArrayList;

import javax.swing.JEditorPane;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JScrollPane;

import javafx.application.Platform;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.embed.swing.JFXPanel;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebEvent;
import javafx.scene.web.WebView;
 
import javax.swing.*;
import java.awt.*;

/*
 * Gson is released under the Apache 2.0 license.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


/** Here we give a demo client for the poker game available at AIGaming.
 * We use the available API calls which can be found on the AIGaming REST API 
 * Manual page http://help.aigaming.com/rest-api-manual .
 * We have created a form that can be used to invoke these calls in order to
 * interact with the API.
 *
 * The basic idea is to create a request and response class for each API call,
 * which are used to communicate with the API and update the form.
 * The request classes' fields are the corresponding request parameters' names
 * and the response classes' fields are the corresponding result values' names.
 *
 * For example, for the "Offer Game" call we create class OfferGameReq
 * with fields BotId, BotPassword, MaximumWaitTime, GameStyleId,
 * DontPlayAgainstSameUser, DontPlayAgainstSameBot and OpponentId, and class
 * OfferGameRes with fields Result, GameState, PlayerKey and Balance.
 * 
 * Whenever we press a button to make an API call, a request object is created
 * and sent to the API using the makeAPICall method. The method serializes the
 * object to JSON, sends it to the API and returns the result, again in JSON.
 * The result is then deserialized into a result object (e.g. OfferGameRes),
 * which is used to update the form.
*/

public class MainWindow extends javax.swing.JFrame {
    
    /**
     * We use the Gson object to serialize objects into JSON format and
     * deserialize JSON strings back into the corresponding objects.
     * 
     * .serializeNulls() allows the Gson instance to output null values
     * .setPrettyPrinting() allows the Gson instance to output indented JSON text.
     * 
     * For more information: https://sites.google.com/site/gson/gson-user-guide
     */
    final Gson gson = new GsonBuilder()
            .serializeNulls()
            .setPrettyPrinting()
            .create();
    
    private final String DEFAULTURL = "https://19y3lnjoy9.execute-api.eu-west-2.amazonaws.com/prod/";
    
    private String playerKey = "";
    private int round = -1;
    private Boolean resetBets = false;
    private Boolean isWaitingForGame = false;
    private Boolean isAutoPlaying = false;
    private AutoPlayWorker autoPlayWorker;
	private int numberOfGames = 0;
    private int numGamesPlayed = 0;
    private int balance;
    

    /**
     * Creates new form MainWindow
     */
    public MainWindow() {
        initComponents();
        resetComponents();
    }
    
    /**
     * The GameState class represents the GameType 3: Texas Hold'Em game state
     * as described on http://help.aigaming.com/rest-api-manual
     */
    public class GameState {
    	public ArrayList<Integer> Ships;
    	public Boolean IsMover;
    	public int Round;
    	public int MyScore;
    	public int OppScore;
    	public long ResponseDeadline;
    	public String GameStatus;
    	public ArrayList<ArrayList<String>> MyBoard;
    	public ArrayList<ArrayList<String>> OppBoard;
    	
		public String GameId;
		public String OpponentId;
    }

    /**
     * Create one request class and one result class for each available API call.
     */
    public class OfferGameReq {
        public String BotId;
        public String BotPassword;
        public Object MaximumWaitTime;
        public int GameStyleId;
        public Boolean DontPlayAgainstSameUser;
        public Boolean DontPlayAgainstSameBot;
        public Object OpponentId;
    }

    public class OfferGameRes {
        public String Result;
        public GameState GameState;
        public String PlayerKey;
        public int Balance;
    }
    
    public class CancelGameOfferReq {
        public String BotId;
        public String BotPassword;
        public String PlayerKey;
    }

    public class CancelGameOfferRes {
        public String Result;
        public GameState GameState;
        public int Balance;
    }
    
    public class PollForGameStateReq {
        public String BotId;
        public String BotPassword;
        public int MaximumWaitTime;
        public String PlayerKey;
    }

    public class PollForGameStateRes {
        public String Result;
        public GameState GameState;
    }
    
    public class MakeMoveReq {
        public String BotId;
        public String BotPassword;
        public String PlayerKey;
        public MoveType Move;
    }

    public class MoveType {
        public ArrayList<ShipPosition> Placement = new ArrayList<ShipPosition>();
        public String Row;
        public int Column;
    }

    public class MakeMoveRes {
        public String Result;
        public GameState GameState;
    }
    
    public class GetListOfGameStylesReq {
        public String BotId;
        public String BotPassword;
        public int GameTypeId;
    }
    
    public class FetchVisualReq {
        public String PlayerKey;
    }
    
    public class FetchVisualRes {
        public String Result;
        public String Html;
    }

    /**
     * GameStyle class as described on
     * http://help.aigaming.com/rest-api-manual#GetListOfGameStyles
     */
    public class GameStyle {
        public int GameStyleId;
        public int GameType;
        public int Stake;
        public int Prize;
        public int MoveTime;
        public int Parameter1;
        public int Parameter2;
        public int Playing;
        public int Waiting;
        
        public String toString() {
            return "id: " + GameStyleId + " / " + Stake
                     + " / " + MoveTime + " ms" + " / " + Playing + " playing, "
                    + Waiting + " waiting";
        }
    }

    public class GetListOfGameStylesRes {
        public String Result;
        public List<GameStyle> GameStyles;
        public int Balance;
    }

    private void createScene() {
        Platform.runLater(new Runnable() {
            @Override 
            public void run() {
                WebView view = new WebView();
                engine = view.getEngine();
                jfxPanel.setScene(new Scene(view));
            }
        });
    }
    public void loadHtml(final String html) {
    	Platform.runLater(new Runnable() {
            @Override 
            public void run() {
                engine.loadContent(html);
            }
        });
    }
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">                          
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        jPanel2 = new javax.swing.JPanel();
        
        jPanel3 = new javax.swing.JPanel();
        txtVS = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        txtId = new javax.swing.JTextField();
        lblPwd = new javax.swing.JLabel();
        txtPwd = new javax.swing.JPasswordField();
        btnLogin = new javax.swing.JButton();
        btnLogout = new javax.swing.JButton();
        txtBalance = new javax.swing.JLabel();
        jLabel8 = new javax.swing.JLabel();
        jLabel9 = new javax.swing.JLabel();
        txtOpp = new javax.swing.JTextField();
        chkDontPlaySameAcc = new javax.swing.JCheckBox();
        jLabel10 = new javax.swing.JLabel();
        jScrollPane2 = new javax.swing.JScrollPane();
        listGameStyles = new javax.swing.JList<>();
        btnRefreshGameStyles = new javax.swing.JButton();
        jLabel11 = new javax.swing.JLabel();
        txtThinkingTime = new javax.swing.JTextField();
        chkPlayAnotherGame = new javax.swing.JCheckBox();
        txtNumberOfGames = new javax.swing.JTextField();
        lblNumGamesPlayed = new javax.swing.JLabel();
        lblMaxLoss = new javax.swing.JLabel();
        btnCancelGame = new javax.swing.JButton();
        jSeparator1 = new javax.swing.JSeparator();
        txtResult = new javax.swing.JLabel();
        jfxPanel = new JFXPanel();

        createScene();
        
        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setResizable(false);

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));
        jPanel1.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0), 2));

        jPanel2.setBackground(new java.awt.Color(0, 128, 0));
        jPanel2.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0), 3));
        jPanel2.setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());

        jPanel3.setBackground(new java.awt.Color(255, 255, 255));
        jPanel3.setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());

        txtVS.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        txtVS.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        txtVS.setText("player vs. opponent");
        jPanel3.add(txtVS, new org.netbeans.lib.awtextra.AbsoluteConstraints(130, 20, 220, -1));

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jfxPanel,javax.swing.GroupLayout.DEFAULT_SIZE,1100,javax.swing.GroupLayout.DEFAULT_SIZE)
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jfxPanel,javax.swing.GroupLayout.DEFAULT_SIZE,600,javax.swing.GroupLayout.DEFAULT_SIZE)
                .addContainerGap(27, Short.MAX_VALUE))
        );

        jLabel5.setText("Bot ID:");

        lblPwd.setText("Password: ");

        btnLogin.setText("Login");
        btnLogin.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnLoginActionPerformed(evt);
            }
        });

        btnLogout.setText("Logout");
        btnLogout.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnLogoutActionPerformed(evt);
            }
        });

        txtBalance.setText("Balance: ");

        jLabel8.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        jLabel8.setText("Game Style Selection");

        jLabel9.setText("Specify Opponent (optional):");

        chkDontPlaySameAcc.setText("Don't play another bot in same user account as me");

        jLabel10.setText("Double click game style line to play");

        listGameStyles.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        listGameStyles.setToolTipText("");
        listGameStyles.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                listGameStylesMouseClicked(evt);
            }
        });
        jScrollPane2.setViewportView(listGameStyles);

        btnRefreshGameStyles.setText("Refresh Game Styles");
        btnRefreshGameStyles.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnRefreshGameStylesActionPerformed(evt);
            }
        });

        jLabel11.setText("Add \"Thinking Time\" (ms):");

        txtThinkingTime.setText("500");
        txtThinkingTime.setToolTipText("");

        chkPlayAnotherGame.setText("Play another game when complete");
        
        txtNumberOfGames.setText("0");
        lblNumGamesPlayed.setText("0 /");
        lblMaxLoss.setText("Maximum Loss:");
        
        txtNumberOfGames.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void removeUpdate(DocumentEvent e) {
            	txtNumberOfGamesActionPerformed();
            }
            @Override
            public void insertUpdate(DocumentEvent e) {
            	txtNumberOfGamesActionPerformed();
            }
            @Override
            public void changedUpdate(DocumentEvent e) {
            	txtNumberOfGamesActionPerformed();
            }
        });

        btnCancelGame.setText("Cancel Game Offer");
        btnCancelGame.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCancelGameActionPerformed(evt);
            }
        });

        txtResult.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        txtResult.setText("Last game result");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                        .addGroup(layout.createSequentialGroup()
                            .addContainerGap()
                            .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(jLabel5)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                        .addComponent(txtId, javax.swing.GroupLayout.PREFERRED_SIZE, 127, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addGap(33, 33, 33)
                                        .addComponent(lblPwd))
                                    .addComponent(jLabel8, javax.swing.GroupLayout.PREFERRED_SIZE, 171, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addGroup(layout.createSequentialGroup()
                                    .addComponent(jLabel9)
                                    .addGap(28, 28, 28)
                                    .addComponent(txtOpp, javax.swing.GroupLayout.PREFERRED_SIZE, 80, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addComponent(chkDontPlaySameAcc, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(jLabel10)
                                .addComponent(jScrollPane2)))
                        .addGroup(layout.createSequentialGroup()
                            .addGap(84, 84, 84)
                            .addComponent(btnRefreshGameStyles))
                        .addGroup(layout.createSequentialGroup()
                            .addContainerGap()
                            .addComponent(jLabel11)
                            .addGap(44, 44, 44)
                            .addComponent(txtThinkingTime, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGroup(layout.createSequentialGroup()
                            .addContainerGap()
                            .addComponent(chkPlayAnotherGame))
                        .addGroup(layout.createSequentialGroup()
                            .addContainerGap()
                            .addGap(21, 21, 21)
                            .addComponent(lblNumGamesPlayed, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(txtNumberOfGames, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addGap(11, 11, 11)
                            .addComponent(lblMaxLoss, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGroup(layout.createSequentialGroup()
                            .addGap(88, 88, 88)
                            .addComponent(btnCancelGame))
                        .addGroup(layout.createSequentialGroup()
                            .addContainerGap()
                            .addComponent(jSeparator1)))
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(txtResult)))
                .addGap(15, 15, 15)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(txtPwd, javax.swing.GroupLayout.PREFERRED_SIZE, 146, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(btnLogout)
                        .addGap(11, 11, 11)
                        .addComponent(btnLogin)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(txtBalance, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(128, 128, 128))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel5)
                    .addComponent(txtId, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(lblPwd)
                    .addComponent(btnLogin)
                    .addComponent(txtBalance)
                    .addComponent(txtPwd, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(btnLogout))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jLabel8)
                        .addGap(18, 18, 18)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jLabel9)
                            .addComponent(txtOpp, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(chkDontPlaySameAcc)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jLabel10)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnRefreshGameStyles)
                        .addGap(21, 21, 21)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jLabel11)
                            .addComponent(txtThinkingTime, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGap(18, 18, 18)
                        .addComponent(chkPlayAnotherGame)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    		.addComponent(lblNumGamesPlayed, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    		.addComponent(txtNumberOfGames, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    		.addComponent(lblMaxLoss, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(btnCancelGame)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jSeparator1, javax.swing.GroupLayout.PREFERRED_SIZE, 10, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(txtResult, javax.swing.GroupLayout.PREFERRED_SIZE, 38, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );

        pack();
    }// </editor-fold>                        

    /** Reset the values of the client's components, ready for login. */
    private void resetComponents() {
        txtId.setText("");
        txtId.setEnabled(true);
        lblPwd.setVisible(true);
        txtPwd.setText("");
        txtPwd.setVisible(true);
        txtBalance.setText("Balance: ");
        txtOpp.setText("");
        txtThinkingTime.setText("500");
        txtVS.setVisible(false);
        txtResult.setVisible(false);
        txtResult.setText("");
        btnLogin.setVisible(true);
        btnLogout.setVisible(false);
        btnCancelGame.setVisible(false);
        chkDontPlaySameAcc.setSelected(false);
        chkPlayAnotherGame.setSelected(false);
        txtNumberOfGames.setText("0");
        lblNumGamesPlayed.setText("0 /");
        lblMaxLoss.setText("Maximum Loss: ");
        listGameStyles.setModel(new javax.swing.DefaultListModel());
        
        playerKey = "";
        isWaitingForGame = false;
        isAutoPlaying = false;
        numGamesPlayed = 0;
    }
    
    private void updateGameResult(GameState gs) {
        String result;
        System.out.println("GameId:" + gs.GameId);
        switch(gs.GameStatus) {
            case "WON": case "WON_BY_TIMEOUT":
                result = "won"; break;
            case "LOST": case "LOST_BY_TIMEOUT":
                result = "lost"; break;
            case "DRAWN":
                result = "has drawn"; break;
            default: return;
        }
        //txtResult = new javax.swing.JLabel("Last game ("+gs.GameId+") result: This bot "+result+
        //        " against"+gs.OpponentId+" ("+gs.GameStatus+")", javax.swing.SwingConstants.CENTER);
        txtResult.setText("<html>Last game ("+gs.GameId+") result: This bot "+result+
               " against<br>"+gs.OpponentId+" ("+gs.GameStatus+")</html>");
        txtResult.setVisible(true);
    }
    
    /**
     * Make an http call to the specified url using the information provided by
     * the req object.
     */
    private String makeAPICall(String url, Object req) {
        // Update the request text field in the form with the corresponding
        // request information and set the response text field to empty string.
        try {       
            // Save the start time of the call in order to output the total time
            // it takes to complete the communication with the API.
            long startTime = System.currentTimeMillis();
            
            // Create a connection to the specified URL.
            URL obj = new URL(url);
            HttpURLConnection con = (java.net.HttpURLConnection) obj.openConnection();

            // We are going to send a POST request with parameters in JSON
            // format and receive a response in JSON.
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            con.setRequestProperty("Accept", "application/json");

            // Get the JSON parameters from the request object.
            String urlParameters = gson.toJson(req);
        	System.out.println("AAA:" + urlParameters);
            // Send the request.
            con.setDoOutput(true);
            DataOutputStream wr = new DataOutputStream(con.getOutputStream());
            wr.writeBytes(urlParameters);
            wr.flush();
            wr.close();

            // Get the response code and initialise variables for the response.
            int responseCode = con.getResponseCode();
            StringBuffer response = new StringBuffer();
            BufferedReader in = null;
            
            // If he response code is 200 then read from the input stream;
            // otherwise, read from the error stream.
            try {
            	in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            } catch (Exception exception) {
                if (responseCode != 200) {
                	in = new BufferedReader(new InputStreamReader(con.getErrorStream()));
                }
            }
            
            // Read the response.
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
            }
            in.close();
            
            // Calculate the elapsed time for the whole communication.
            long stopTime = System.currentTimeMillis();
            long elapsedTime = stopTime - startTime;
            System.out.println("AAA2:" + response.toString());
            // Update the response box in the form and return the JSON response.
            return response.toString();
            
        } catch (Exception exception) {
            return (exception.getMessage());
        }
    }
    
    /**
     * A helper method that makes the "Poll For Game State" call and updates the
     * form.
     */
    PollForGameStateRes pollForGameState(String id, String pwd, String key) {
        // Create a request object.
        PollForGameStateReq req = new PollForGameStateReq();
        req.BotId = id;
        req.BotPassword = pwd;
        req.PlayerKey = key;
        // Make and API call and update the form.
        String resJson = makeAPICall(DEFAULTURL+"GM-PollForGameState", req);
        System.out.println("BBB:" + resJson);
        PollForGameStateRes res = gson.fromJson(resJson, PollForGameStateRes.class);
        
        FetchVisualReq reqVis = new FetchVisualReq();
        reqVis.PlayerKey = key;
        String resVisJson = makeAPICall(DEFAULTURL+"FetchVisual", reqVis);
        FetchVisualRes resVis = gson.fromJson(resVisJson, FetchVisualRes.class);
        
        if(resVis.Result.equals("SUCCESS")) loadHtml(resVis.Html);
        return res;
    }
    
    /**
     * A helper method that makes the "Make Move" call and updates the
     * form.
     */
    MakeMoveRes makeMove(String id, String pwd, String key, ArrayList<ShipPosition> placement, String row, int column) {
        // Create a request object.
        MakeMoveReq req = new MakeMoveReq();
        req.BotId = id;
        req.BotPassword = pwd;
        req.PlayerKey = key;
        req.Move = new MoveType();
        req.Move.Placement = placement;
        req.Move.Row = row;
        req.Move.Column = column;

        // Make and API call
        String resJson = makeAPICall(DEFAULTURL+"GM-MakeMove", req);
        MakeMoveRes res = gson.fromJson(resJson, MakeMoveRes.class);
        
        
        FetchVisualReq reqVis = new FetchVisualReq();
        reqVis.PlayerKey = key;
        String resVisJson = makeAPICall(DEFAULTURL+"FetchVisual", reqVis);
        FetchVisualRes resVis = gson.fromJson(resVisJson, FetchVisualRes.class);
        
        if(resVis.Result.equals("SUCCESS")) loadHtml(resVis.Html);
        return res;
    }

    /** Swing Worker helper class that allows us to play the game in a separate thread. */
    class AutoPlayWorker extends javax.swing.SwingWorker<Void, GameState> {
        private int GameStyleId;
        
        private GameState offerAndWaitForGame() {
            // Offer a game.
            String result = offerGame(GameStyleId);
            if(result.equals("Invited Bot Not Existing")) return null;
            
            // Hide the last result
            txtResult.setVisible(false);
            // Show the cancel game button since the player is waiting for a game.
            btnCancelGame.setText("Cancel Game");
            isWaitingForGame = true;        
            btnCancelGame.setVisible(true);
            // Poll for the game state initially and play only if the result is
            // "SUCCESS", i.e, if we are taking part in a game.
            PollForGameStateRes pfgsres;
            String Result = "";
            do {
                pfgsres = pollForGameState(txtId.getText(), String.valueOf(txtPwd.getPassword()), playerKey);
                Result = pfgsres.Result;
            } while(Result.equals("WAITING_FOR_GAME") && isWaitingForGame);
            if (!Result.equals("SUCCESS")) {
            	return null;
            }
            GameState gs = pfgsres.GameState;
            publish(gs);
            return gs;
        }
        
        private void autoPlayGame(GameState gs) {
            // Now a game has started so change the cancel game button to "Stop Game".
            btnCancelGame.setText("Stop Game");
            // Display the label  "player vs opponent" above the board.
            txtVS.setText(txtId.getText()+" vs "+gs.OpponentId);
            txtVS.setVisible(true);
            isWaitingForGame = false;
            isAutoPlaying = true;
            
            PollForGameStateRes pfgsres;
            String Result = "";
            
            // Play until possible; the loop breaks if the game is over.
            while(isAutoPlaying) {
                // If it is our turn, send a move request and update the form.
            	System.out.println("Making Moves WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW");
            	System.out.println("CCC:" + gs);
                if (gs.IsMover) {

                    try {
                        // Wait for the specified thinking time.
                        int thinkingTime = 0;
                        try {
                            thinkingTime = (int) Double.parseDouble(txtThinkingTime.getText());
                            if(thinkingTime < 0) thinkingTime = 0;
                        } catch(Exception e) {}
                        Thread.sleep(thinkingTime);
                        
                        BattleshipsMove move = Battleships.calculateMove(gs);
                        
                        // Make the move.
                        MakeMoveRes mmres = makeMove(txtId.getText(), String.valueOf(txtPwd.getPassword()), playerKey, move.Placement, move.Row, move.Column);
                        Result = mmres.Result;
                        // Terminate the loop if the request was unsuccessful or if
                        // the game is not running anymore.
                        if(Result.equals("INVALID_MOVE")) {
                        	System.out.println("DDD:" + move);
                        }
                        
                        if (!Result.equals("SUCCESS")) {
                        	System.out.println("22");
                        	break;
                        }
                        gs = mmres.GameState;
                        publish(gs);
                        if (!gs.GameStatus.equals("RUNNING")) {
                        	System.out.println("33");
                        	break;
                        }
                    } catch (Exception exception) {
                        System.err.println("Caught Exception: " + exception.getMessage());
                    }
                }
                // If it is not our turn, poll for the game state and update it if 
                // the poll request was successful. Otherwise, terminate the loop.
                else {
                    pfgsres = pollForGameState(txtId.getText(), String.valueOf(txtPwd.getPassword()), playerKey);
                    Result = pfgsres.Result;
                    gs = pfgsres.GameState;
                    publish(gs);
                    if (!Result.equals("SUCCESS")) break;
                }
            }
            // Refresh the game styles and balance
            refreshGameStyles();
            // Update the game result
            updateGameResult(gs);
            //Increment number of games played
            numGamesPlayed ++;
            lblNumGamesPlayed.setText(numGamesPlayed + " /");
        }
        
        public AutoPlayWorker(int GameStyleId) {
            this.GameStyleId = GameStyleId;
        }
        
        @Override
        protected Void doInBackground() {
            do {
                GameState gs = offerAndWaitForGame();
                if(gs == null) return null;
                autoPlayGame(gs);
            } while(chkPlayAnotherGame.isSelected() && isAutoPlaying && (numberOfGames == 0 || numGamesPlayed < numberOfGames));
            return null;
        }
        
        @Override
        protected void process(List<GameState> gameStates) {
            //for(GameState gs : gameStates) loadHtml("");
        }
    }
    
    /**
     * This method performs an "Offer Game" call to the API
     * and updates the form based on the result.
     */
	private String offerGame(int GameStyleId) {                                             
        // Create a new OfferGameReq object and initialise it with the current
        // values from the form.
        OfferGameReq req = new OfferGameReq();
        req.BotId = txtId.getText();
        req.BotPassword = String.valueOf(txtPwd.getPassword());
//        req.GameStyleId = (int) Double.parseDouble(txtStyle.getText());
        req.GameStyleId = GameStyleId;

        req.DontPlayAgainstSameBot = null;
        req.DontPlayAgainstSameUser = chkDontPlaySameAcc.isSelected();
        if (!(txtOpp.getText().equals("")))
            req.OpponentId = txtOpp.getText();

        // Make an "Offer Game" API call with the request object to the current
        // URL in the form.
        String result = makeAPICall(DEFAULTURL + "GM-OfferGame", req);
        
        // result is in JSON format, so we need to deserialise it into
        // OfferGameRes object.
        OfferGameRes res = gson.fromJson(result, OfferGameRes.class);
        
        playerKey = res.PlayerKey;
        return res.Result;
    }
    
     /**
     * This method performs a "Cancel Game Offer" call to the API
     * and updates the form based on the result.
     * It is completely analogous to the "Offer Game" call.
     */
    private void cancelGameOffer() {                                                   
        // Create a request object.
        CancelGameOfferReq req = new CancelGameOfferReq();
        req.BotId = txtId.getText();
        req.BotPassword = String.valueOf(txtPwd.getPassword());
        req.PlayerKey = playerKey;

        // Make and API call and update the form.
        String resJson = makeAPICall(DEFAULTURL + "GM-CancelGameOffer", req);
        CancelGameOfferRes res = gson.fromJson(resJson, CancelGameOfferRes.class);
        
        playerKey = "";
    }     
    
    
    private void refreshGameStyles() {
        // Create a request object.
        GetListOfGameStylesReq req = new GetListOfGameStylesReq();
        req.BotId = txtId.getText();
        req.BotPassword = String.valueOf(txtPwd.getPassword());
        req.GameTypeId = 51;

        // Make and API call and update the form.
        String resJson = makeAPICall(DEFAULTURL + "GM-GetListOfGameStyles", req);
        GetListOfGameStylesRes res = gson.fromJson(resJson, GetListOfGameStylesRes.class);
        
        // Update the form if the request was successful.
        if(!res.Result.equals("SUCCESS")) return;
        // Update the balance.
        balance = res.Balance;
        txtBalance.setText("Balance: " + balance);
        // Update the list of game styles.
        javax.swing.DefaultListModel listModel = new javax.swing.DefaultListModel();
        for(GameStyle gs : res.GameStyles) listModel.addElement(gs.toString());
        listGameStyles.setModel(listModel);
    }    

    private void btnLoginActionPerformed(java.awt.event.ActionEvent evt) {                                         
        // Login by making a "Get List Of Game Styles" call to the API.
        
        // Create a request object.
        GetListOfGameStylesReq req = new GetListOfGameStylesReq();
        req.BotId = txtId.getText();
        req.BotPassword = String.valueOf(txtPwd.getPassword());
        req.GameTypeId = 51;

        // Make and API call and update the form.
        String resJson = makeAPICall(DEFAULTURL + "GM-GetListOfGameStyles", req);
        GetListOfGameStylesRes res = gson.fromJson(resJson, GetListOfGameStylesRes.class);

        // Update the form if the request was successful.
        if(!res.Result.equals("SUCCESS")) return;
        // Disable the user id field, hide the password and swap the login/logout buttons.
        txtId.setEnabled(false);
        lblPwd.setVisible(false);
        txtPwd.setVisible(false);
        btnLogin.setVisible(false);
        btnLogout.setVisible(true);
        // Update the balance.
        System.out.println(res);
        balance = res.Balance;
        txtBalance.setText("Balance: " + balance);
        // Update the list of game styles.
        javax.swing.DefaultListModel listModel = new javax.swing.DefaultListModel();
        for(GameStyle gs : res.GameStyles) listModel.addElement(gs.toString());
        listGameStyles.setModel(listModel);
    }

    private void listGameStylesMouseClicked(java.awt.event.MouseEvent evt) {                                            
        // Make a game offer if an item of the list is double clicked and
        // the player is not waiting or playing.
    	
    	numGamesPlayed = 0; //Reset the number of games played
    	lblNumGamesPlayed.setText(numGamesPlayed + " /");
    	lblMaxLoss.setText("Maximum Loss: " + Math.min(balance, numberOfGames));
        javax.swing.JList listGameStyles = (javax.swing.JList) evt.getSource();
        if(evt.getClickCount() != 2 || isWaitingForGame || isAutoPlaying) return;
        int index = listGameStyles.locationToIndex(evt.getPoint());
        if (index < 0) return;
        
        // Disable the list selection.
        listGameStyles.setCellRenderer(new javax.swing.DefaultListCellRenderer() {
            @Override
            public Component getListCellRendererComponent(JList list, Object value, int index,
                    boolean isSelected, boolean cellHasFocus) {
                super.getListCellRendererComponent(list, value, index, false, false);
                return this;
            }
        });

        // Get the selected item.
        Object o = listGameStyles.getModel().getElementAt(index);

        // Offer a game.
        int GameStyleId = Integer.parseInt(o.toString().split("id: ")[1].split(" /")[0]);

        // Start the game in another thread.
        autoPlayWorker = new AutoPlayWorker(GameStyleId);
        autoPlayWorker.execute();
    }

    private void btnLogoutActionPerformed(java.awt.event.ActionEvent evt) {                                          
        resetComponents();
    }                                         

    private void btnCancelGameActionPerformed(java.awt.event.ActionEvent evt) {                                              
        // If the player is waiting for a game, kill the worker thread,
        // send a "Cancel Game Offer" request to the API and hide the cancel game button.
        if(isWaitingForGame) {
            autoPlayWorker.cancel(true);
            cancelGameOffer();
            btnCancelGame.setVisible(false);
            isWaitingForGame = false;
        }
        // If the player is playing, kill the worker thread, send a "Cancel Game Offer"
        // request to the API and hide the cancel game button.
        else if(isAutoPlaying) {
            autoPlayWorker.cancel(true);
            btnCancelGame.setVisible(false);
            btnCancelGame.setText("Cancel Game Offer");
            isAutoPlaying = false;
        }
    }                                             

    private void btnRefreshGameStylesActionPerformed(java.awt.event.ActionEvent evt) {                                                     
        refreshGameStyles();
    }

    private void txtNumberOfGamesActionPerformed() {                                                     
        try {
        	numberOfGames = (int) Double.parseDouble(txtNumberOfGames.getText());
            if(numberOfGames < 0) numberOfGames = 0;
        } catch(Exception e) {}
        lblMaxLoss.setText("Maximum Loss: " + Math.min(balance, numberOfGames));
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new MainWindow().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify                     
    private javax.swing.JButton btnCancelGame;
    private javax.swing.JButton btnLogin;
    private javax.swing.JButton btnLogout;
    private javax.swing.JButton btnRefreshGameStyles;
    private javax.swing.JCheckBox chkDontPlaySameAcc;
    private javax.swing.JCheckBox chkPlayAnotherGame;
    private javax.swing.JLabel lblNumGamesPlayed;
    private javax.swing.JTextField txtNumberOfGames;
    private javax.swing.JLabel lblMaxLoss;
    private javax.swing.JLabel jLabel10;
    private javax.swing.JLabel jLabel11;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JLabel jLabel9;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel3;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JSeparator jSeparator1;
    private javax.swing.JLabel lblPwd;
    private javax.swing.JList<String> listGameStyles;
    private javax.swing.JLabel txtBalance;
    private javax.swing.JTextField txtId;
    private javax.swing.JTextField txtOpp;
    private javax.swing.JPasswordField txtPwd;
    private javax.swing.JLabel txtResult;
    private javax.swing.JTextField txtThinkingTime;
    private javax.swing.JLabel txtVS;
	private JFXPanel jfxPanel;
    private WebEngine engine;
    
    // End of variables declaration                   
}
