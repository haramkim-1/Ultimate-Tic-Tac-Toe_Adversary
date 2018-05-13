package com.theaigames.tictactoe;

import java.util.ArrayList;
import java.util.List;

import com.theaigames.engine.io.Bot;
import com.theaigames.engine.io.IOPlayer;
import com.theaigames.game.AbstractGame;
import com.theaigames.tictactoe.field.Field;
import com.theaigames.tictactoe.player.Player;

public class Tictactoe extends AbstractGame {
	
	private final int TIMEBANK_MAX = Integer.MAX_VALUE;
	private final int TIME_PER_MOVE = Integer.MAX_VALUE;
	private List<Player> players;

	@Override
	public void setupGame(ArrayList<Bot> players) throws Exception {

		System.out.println("Setting up game...");

		// create all the players and everything they need
		this.players = new ArrayList<>();

		// create the playing field
		Field mField = new Field();

		for(int i=0; i<players.size(); i++) {
			// create the player
			String playerName = String.format("player%d", i+1);
			Player player = new Player(playerName, players.get(i), TIMEBANK_MAX, TIME_PER_MOVE, i+1);
			this.players.add(player);

		}
		this.players.forEach(this::sendSettings);

		// create the processor
		super.processor = new Processor(this.players, mField, LOG_MOVES);
	}

	private void sendSettings(Player player) {
		String playerString = "player1,player2";

		player.sendSetting("timebank", TIMEBANK_MAX);
		player.sendSetting("time_per_move", TIME_PER_MOVE);
		player.sendSetting("player_names", playerString);
		player.sendSetting("your_bot", player.getName());
		player.sendSetting("your_botid", player.getId());
	}

	@Override
	protected void runEngine() throws Exception {
	    System.out.println("starting...");
	    
		super.engine.setLogic(this);
		super.engine.start();
	}
	
	public static void main(String args[]) throws Exception {
		Tictactoe game = new Tictactoe();
		
		game.DEV_MODE = false;
		game.TEST_BOT = "java -cp /home/jim/workspace/tictactoe-starterbot/bin/ bot.BotStarter";
		game.NUM_TEST_BOTS = 2;
		
		game.setupEngine(args);
		game.runEngine();
	}
}
