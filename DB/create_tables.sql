CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    priority character varying,
    last_completed date,
    repeat_interval integer,
    user_id integer NOT NULL,
    next_due date GENERATED ALWAYS AS ((last_completed + ((repeat_interval)::double precision * '1 day'::interval))) STORED
);


ALTER TABLE public.tasks OWNER TO housework_admin;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: housework_admin
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO housework_admin;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: housework_admin
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


CREATE TABLE public.task_tags (
    task_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.task_tags OWNER TO housework_admin;

--
-- Name: task_tags task_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.task_tags
    ADD CONSTRAINT task_tags_pkey PRIMARY KEY (task_id, tag_id);


--
-- Name: task_tags task_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.task_tags
    ADD CONSTRAINT task_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: task_tags task_tags_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.task_tags
    ADD CONSTRAINT task_tags_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.tags OWNER TO housework_admin;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: housework_admin
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_id_seq OWNER TO housework_admin;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: housework_admin
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: housework_admin
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);

