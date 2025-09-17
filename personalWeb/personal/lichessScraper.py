import lichess
import lichess.api
from lichess.format import PGN, JSON
import streamlit as st


class LichessScraper:
    '''
    Scrapes Lichess.org for user data and information
    Uses the streamlit library to render to webpage.
    command: [streamlit run lichessScraper.py]
    note: command should be run in the same directory as the project
    '''
    def __init__(self) -> None:
        # default streamlit application
        st.title("Lichess Games Analyser")
        self.username = st.text_input("Lichess username")

        if st.button("Fetch games"):
            if self.username:
                games = self.fetch_recent_games(self.username)
                count = 1
                # lenght = len(list(games))
                if games:
                    st.write(f"Recent games for {self.username}:")
                    for game in games:
                        try:
                            st.write(f"{count}: Game:=> {game['players']} ::: Winner:=> {game['winner']}") # select player games info
                        except Exception as e:
                            st.write(f"{count}: game drawn")
                            count += 1
                            continue
                        count += 1
                    st.write("Eof")
                    count = 1
                else:
                    st.write("No games found")
            else:
                st.write("Username not found")
        else:
            st.warning("Please enter a username")


    def fetch_recent_games(self, username):
        '''
        get the user's most recent games from lichess
        '''
        try:
           games = lichess.api.user_games(username, max=20)
           return list(games)
        except Exception as e:
            st.write(f"Error fetching games:=> {e}")
            return []


if __name__=='__main__':
    # Run the scaper
    LichessScraper()